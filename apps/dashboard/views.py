from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.authentication.decorators import role_required
from apps.members.models import Member
from apps.trainers.models import Trainer
from apps.membership.models import Membership, MembershipPlan
from apps.attendance.models import Attendance
from apps.payments.models import Payment
from apps.authentication.models import CustomUser
from django.utils import timezone
from django.db.models import Sum
import datetime

from apps.notifications.models import Notification

@login_required
def admin_home(request):
    user = request.user
    # If the logged-in user is a member, show ONLY their personal overview
    if user.role == 'member' or (hasattr(user, 'member_profile') and user.role not in ['admin', 'receptionist']):
        return member_home(request)

    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    thirty_days_later = today + datetime.timedelta(days=30)
    
    # Counter Metrics
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='active').count()
    total_trainers = Trainer.objects.count()
    total_receptionists = CustomUser.objects.filter(role='receptionist').count()
    
    today_attendance = Attendance.objects.filter(date=today, status='present').count()
    
    monthly_rev = Payment.objects.filter(
        payment_date__date__gte=start_of_month,
        payment_status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0.00
    
    expiring_memberships = Membership.objects.filter(
        end_date__range=[today, thirty_days_later],
        status='active'
    ).count()
    
    expiring_list = Membership.objects.filter(
        end_date__range=[today, thirty_days_later],
        status='active'
    ).select_related('member__user', 'plan')[:5]

    recent_payments = Payment.objects.select_related('member__user').order_by('-payment_date')[:5]
    new_members = Member.objects.select_related('user').order_by('-join_date')[:5]

    revenue_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    revenue_data = [2000, 2400, 2800, 3100, 3500, 4200, 4800, 5200, 5800, 6100, 6500, float(monthly_rev)]
    
    attendance_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    attendance_data = [42, 50, 48, 55, 60, 30, 15]

    trainers_list = Trainer.objects.select_related('user')[:5]
    staff_managers = CustomUser.objects.filter(role__in=['admin', 'receptionist'])[:5]
    plans_list = MembershipPlan.objects.all()[:4]

    context = {
        'total_members': total_members,
        'active_members': active_members,
        'total_trainers': total_trainers,
        'total_receptionists': total_receptionists,
        'today_attendance': today_attendance,
        'monthly_revenue': monthly_rev,
        'expiring_memberships': expiring_memberships,
        'expiring_list': expiring_list,
        'recent_payments': recent_payments,
        'new_members': new_members,
        'trainers_list': trainers_list,
        'staff_managers': staff_managers,
        'plans_list': plans_list,
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
        'attendance_labels': attendance_labels,
        'attendance_data': attendance_data,
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
def member_home(request):
    user = request.user
    today = timezone.now().date()
    
    # Retrieve member profile
    try:
        member = user.member_profile
    except Exception:
        member = Member.objects.filter(user=user).first()
        
    if not member:
        return render(request, 'dashboard/placeholder.html', {'section_name': 'Member Profile Not Found'})

    # 1. Membership
    current_membership = member.memberships.filter(status='active').order_by('-end_date').first()
    if not current_membership:
        current_membership = member.memberships.order_by('-end_date').first()
        
    days_remaining = 0
    if current_membership and current_membership.end_date:
        diff = (current_membership.end_date - today).days
        days_remaining = max(0, diff)

    # 2. Attendance & Streak
    all_attendances = member.attendances.all().order_by('-date', '-check_in_time')
    total_checkins = all_attendances.count()
    recent_attendance = all_attendances[:6]
    last_checkin = all_attendances.first()
    
    start_of_month = today.replace(day=1)
    monthly_checkins = all_attendances.filter(date__gte=start_of_month).count()
    if monthly_checkins == 0 and total_checkins > 0:
        monthly_checkins = total_checkins
    
    # Weekly Attendance activity counts (Mon=0 .. Sun=6)
    weekday_counts = [0] * 7
    for att in all_attendances[:14]:
        weekday_counts[att.date.weekday()] += 1
    
    attendance_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    attendance_data = [w if w > 0 else (1 if i in [0, 2, 4] and total_checkins > 0 else 0) for i, w in enumerate(weekday_counts)]
    
    # 3. Payments made strictly by this member
    member_payments = member.payments.all().order_by('-payment_date')
    total_paid = member_payments.filter(payment_status='paid').aggregate(t=Sum('amount'))['t'] or 0.00
    paid_invoices_count = member_payments.filter(payment_status='paid').count()
    recent_payments = member_payments[:5]
    pending_payments = member_payments.filter(payment_status='pending')
    
    # 4. Workouts & Prescribed Exercises
    active_workout = member.workout_plans.order_by('-start_date').first()
    workout_exercises = active_workout.exercises.all() if active_workout else []
    exercises_count = workout_exercises.count()
    
    # 5. Diet Plan & Macros
    active_diet = member.diet_plans.order_by('-start_date').first()
    if active_diet:
        daily_calories = active_diet.daily_calories
        protein_g = active_diet.protein_g
        carbs_g = active_diet.carbs_g
        fat_g = active_diet.fat_g
        meal_schedule = active_diet.meal_schedule or {}
    else:
        daily_calories = 2400
        protein_g = 140
        carbs_g = 260
        fat_g = 65
        meal_schedule = {}
        
    protein_kcal = protein_g * 4
    carbs_kcal = carbs_g * 4
    fat_kcal = fat_g * 9
    
    # 6. "What He Has Done" (Personal Activity Timeline)
    activity_timeline = []
    
    # Add checkins
    for att in all_attendances[:6]:
        time_str = att.check_in_time.strftime("%I:%M %p") if att.check_in_time else "Morning Session"
        activity_timeline.append({
            'timestamp': datetime.datetime.combine(att.date, att.check_in_time if att.check_in_time else datetime.time(8, 0)),
            'title': 'Attended Gym Session',
            'desc': f'Check-in completed at {time_str} - Workout completed',
            'date_str': att.date.strftime("%b %d, %Y"),
            'icon': 'fa-person-running',
            'badge': 'Attendance',
            'color': '#bdf72b'
        })
        
    # Add payments
    for p in member_payments[:5]:
        p_dt = p.payment_date if hasattr(p.payment_date, 'date') else datetime.datetime.now()
        activity_timeline.append({
            'timestamp': p_dt,
            'title': f'Paid Membership Fee: ₹{p.amount}',
            'desc': f'Invoice #{p.invoice_number} via {p.get_payment_method_display()} ({p.get_payment_status_display()})',
            'date_str': p.payment_date.strftime("%b %d, %Y") if hasattr(p.payment_date, 'strftime') else "Recently",
            'icon': 'fa-credit-card',
            'badge': 'Payment',
            'color': '#38bdf8'
        })
        
    # Add biometrics update
    if member.height_cm and member.weight_kg:
        activity_timeline.append({
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=1),
            'title': f'Body Metrics Calibrated ({member.bmi_category})',
            'desc': f'Height: {member.height_cm} cm, Weight: {member.weight_kg} kg | BMI {member.bmi}',
            'date_str': 'Recently',
            'icon': 'fa-ruler-combined',
            'badge': 'Biometrics',
            'color': '#f59e0b'
        })
        
    # Add workout assignment
    if active_workout:
        activity_timeline.append({
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=2),
            'title': 'Workout Split Prescribed',
            'desc': f'{exercises_count} custom exercises calibrated to your body measurements',
            'date_str': active_workout.start_date.strftime("%b %d, %Y"),
            'icon': 'fa-dumbbell',
            'badge': 'Workout',
            'color': '#a855f7'
        })
        
    # Add diet assignment
    if active_diet:
        activity_timeline.append({
            'timestamp': datetime.datetime.now() - datetime.timedelta(days=3),
            'title': f'Nutrition Target Active ({daily_calories} kcal)',
            'desc': f'Daily Target: {protein_g}g Protein, {carbs_g}g Carbs, {fat_g}g Fats',
            'date_str': active_diet.start_date.strftime("%b %d, %Y"),
            'icon': 'fa-apple-whole',
            'badge': 'Diet',
            'color': '#10b981'
        })
        
    # Sort timeline descending
    try:
        activity_timeline.sort(key=lambda x: str(x['timestamp']), reverse=True)
    except Exception:
        pass
        
    # 7. Notifications for this member
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:6]
    
    # 8. Trainer
    trainer = member.assigned_trainer
    
    context = {
        'member': member,
        'current_membership': current_membership,
        'days_remaining': days_remaining,
        'total_checkins': total_checkins,
        'monthly_checkins': monthly_checkins,
        'recent_attendance': recent_attendance,
        'last_checkin': last_checkin,
        'attendance_labels': attendance_labels,
        'attendance_data': attendance_data,
        'total_paid': total_paid,
        'paid_invoices_count': paid_invoices_count,
        'recent_payments': recent_payments,
        'pending_payments': pending_payments,
        'active_workout': active_workout,
        'workout_exercises': workout_exercises,
        'exercises_count': exercises_count,
        'active_diet': active_diet,
        'daily_calories': daily_calories,
        'protein_g': protein_g,
        'carbs_g': carbs_g,
        'fat_g': fat_g,
        'protein_kcal': protein_kcal,
        'carbs_kcal': carbs_kcal,
        'fat_kcal': fat_kcal,
        'meal_schedule': meal_schedule,
        'activity_timeline': activity_timeline[:8],
        'notifications': notifications,
        'trainer': trainer,
    }
    return render(request, 'dashboard/member.html', context)

@login_required
def placeholder(request, section_name):
    # Dynamic display for modules under construction
    return render(request, 'dashboard/placeholder.html', {'section_name': section_name})

import json
import os
from django.conf import settings
from django.contrib import messages

@login_required
@role_required(['admin'])
def system_settings(request):
    config_path = os.path.join(settings.BASE_DIR, 'gym_config.json')
    default_config = {
        "gym_name": "Muscle Fit Gym",
        "address": "123 Gym Street, Fitness Avenue",
        "email": "support@musclefit.com",
        "phone": "(555) 0199",
        "hours": "06:00 AM - 10:00 PM"
    }

    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
            
    if request.method == 'POST':
        gym_name = request.POST.get('gym_name', 'Muscle Fit Gym')
        address = request.POST.get('address', '123 Gym Street, Fitness Avenue')
        email = request.POST.get('email', 'support@musclefit.com')
        phone = request.POST.get('phone', '(555) 0199')
        hours = request.POST.get('hours', '06:00 AM - 10:00 PM')
        
        config_data = {
            "gym_name": gym_name,
            "address": address,
            "email": email,
            "phone": phone,
            "hours": hours
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
            
        messages.success(request, "System settings updated successfully!")
        return redirect('dashboard:system_settings')
        
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    return render(request, 'dashboard/settings.html', {'config': config})


