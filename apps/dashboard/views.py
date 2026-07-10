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

@login_required
@role_required(['admin'])
def admin_home(request):
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

    # Lists
    recent_payments = Payment.objects.select_related('member__user').order_by('-payment_date')[:5]
    new_members = Member.objects.select_related('user').order_by('-join_date')[:5]

    # Mock Chart Data for dashboard charts (represented as simple lists for Chart.js)
    # We will pass these numbers to feed Chart.js canvases in the template
    revenue_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    revenue_data = [2000, 2400, 2800, 3100, 3500, 4200, 4800, 5200, 5800, 6100, 6500, float(monthly_rev)]
    
    attendance_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    attendance_data = [42, 50, 48, 55, 60, 30, 15]

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
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
        'attendance_labels': attendance_labels,
        'attendance_data': attendance_data,
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
@role_required(['receptionist'])
def reception_home(request):
    today = timezone.now().date()
    
    # Receptionist specific stats
    active_members = Member.objects.filter(status='active').count()
    today_attendance = Attendance.objects.filter(date=today, status='present').count()
    pending_payments_count = Payment.objects.filter(payment_status='pending').count()
    
    recent_members = Member.objects.select_related('user').order_by('-join_date')[:10]
    
    context = {
        'active_members': active_members,
        'today_attendance': today_attendance,
        'pending_payments_count': pending_payments_count,
        'recent_members': recent_members,
    }
    return render(request, 'dashboard/receptionist.html', context)

@login_required
@role_required(['trainer'])
def trainer_home(request):
    # Retrieve trainer profile
    try:
        trainer = request.user.trainer_profile
    except Trainer.DoesNotExist:
        trainer = None
        
    assigned_members_count = 0
    assigned_members = []
    
    if trainer:
        # Fetch members that have workouts or diets assigned by this trainer
        assigned_members = Member.objects.filter(
            workout_plans__trainer=trainer
        ).select_related('user').distinct()[:10]
        assigned_members_count = Member.objects.filter(workout_plans__trainer=trainer).distinct().count()
        
    context = {
        'trainer': trainer,
        'assigned_members_count': assigned_members_count,
        'assigned_members': assigned_members,
    }
    return render(request, 'dashboard/trainer.html', context)

@login_required
@role_required(['member'])
def member_home(request):
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        member = None
        
    current_membership = None
    recent_attendance = []
    payments = []
    active_workout = None
    active_diet = None
    
    if member:
        current_membership = member.memberships.filter(status='active').first()
        recent_attendance = member.attendances.all().order_by('-date')[:5]
        payments = member.payments.all().order_by('-payment_date')[:5]
        active_workout = member.workout_plans.order_by('-start_date').first()
        active_diet = member.diet_plans.order_by('-start_date').first()
        
    context = {
        'member': member,
        'current_membership': current_membership,
        'recent_attendance': recent_attendance,
        'payments': payments,
        'active_workout': active_workout,
        'active_diet': active_diet,
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


