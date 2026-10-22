from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.authentication.decorators import role_required
from apps.members.models import Member
from .models import Attendance
import datetime

@login_required
@role_required(['admin', 'receptionist'])
def daily_attendance(request):
    today = timezone.now().date()
    now_time = timezone.now().time()
    
    # Process check-in / check-out actions
    if request.method == 'POST':
        member_id = request.POST.get('member_pk')
        action = request.POST.get('action') # 'check_in' or 'check_out'
        member = get_object_or_404(Member, pk=member_id)
        
        if action == 'check_in':
            attendance, created = Attendance.objects.get_or_create(
                member=member,
                date=today,
                defaults={'check_in_time': now_time, 'status': 'present'}
            )
            if created:
                messages.success(request, f"Checked in {member.user.get_full_name()} at {now_time.strftime('%I:%M %p')}.")
            else:
                messages.warning(request, f"{member.user.get_full_name()} is already checked in for today.")
        
        elif action == 'check_out':
            attendance = Attendance.objects.filter(member=member, date=today).first()
            if attendance:
                attendance.check_out_time = now_time
                attendance.save()
                messages.success(request, f"Checked out {member.user.get_full_name()} at {now_time.strftime('%I:%M %p')}.")
            else:
                messages.error(request, "No check-in record found for this member today.")
                
        return redirect('attendance:daily_attendance')

    # Fetch members based on role (strictly personal for members)
    if request.user.role == 'member':
        members = Member.objects.filter(user=request.user).select_related('user')
    elif request.user.role == 'trainer':
        members = Member.objects.filter(assigned_trainer__user=request.user).select_related('user')
    else:
        members = Member.objects.all().select_related('user')
    
    # Search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        members = members.filter(
            user__first_name__icontains=search_query) | members.filter(
            user__last_name__icontains=search_query) | members.filter(
            member_id__icontains=search_query)

    # Fetch today's checkins mapping
    today_checkins = {att.member_id: att for att in Attendance.objects.filter(date=today)}

    # Build list with today's status
    member_statuses = []
    for m in members:
        att = today_checkins.get(m.pk)
        member_statuses.append({
            'member': m,
            'attendance': att,
        })

    context = {
        'member_statuses': member_statuses,
        'search_query': search_query,
        'today': today,
    }
    return render(request, 'attendance/daily.html', context)

@login_required
def attendance_history(request):
    user = request.user
    if user.role == 'member':
        attendance_logs = Attendance.objects.filter(member__user=user).order_by('-date', '-check_in_time')
    else:
        attendance_logs = Attendance.objects.all().select_related('member__user').order_by('-date', '-check_in_time')
    
    # Apply Filters
    search_query = request.GET.get('search', '').strip()
    if search_query:
        attendance_logs = attendance_logs.filter(
            member__user__first_name__icontains=search_query) | attendance_logs.filter(
            member__user__last_name__icontains=search_query) | attendance_logs.filter(
            member__member_id__icontains=search_query)
            
    date_query = request.GET.get('date', '').strip()
    if date_query:
        try:
            target_date = datetime.datetime.strptime(date_query, "%Y-%m-%d").date()
            attendance_logs = attendance_logs.filter(date=target_date)
        except ValueError:
            pass

    context = {
        'attendance_logs': attendance_logs,
        'search_query': search_query,
        'date_query': date_query,
    }
    return render(request, 'attendance/history.html', context)

@login_required
@role_required(['admin', 'receptionist'])
def attendance_reports(request):
    # Quick statistics
    today = timezone.now().date()
    total_members = Member.objects.count()
    today_checkins = Attendance.objects.filter(date=today, status='present').count()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_checkins = Attendance.objects.filter(date=yesterday, status='present').count()
    
    # Weekly check-ins average
    last_7_days = [today - datetime.timedelta(days=i) for i in range(7)]
    weekly_stats = []
    for day in reversed(last_7_days):
        count = Attendance.objects.filter(date=day, status='present').count()
        weekly_stats.append({
            'date': day.strftime("%a (%b %d)"),
            'count': count
        })

    context = {
        'total_members': total_members,
        'today_checkins': today_checkins,
        'yesterday_checkins': yesterday_checkins,
        'weekly_stats': weekly_stats,
    }
    return render(request, 'attendance/reports.html', context)
