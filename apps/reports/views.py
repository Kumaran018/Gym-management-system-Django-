from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from apps.authentication.decorators import role_required
from apps.members.models import Member
from apps.trainers.models import Trainer
from apps.attendance.models import Attendance
from apps.payments.models import Payment
from apps.membership.models import MembershipPlan
import datetime

@login_required
@role_required(['admin'])
def reports_index(request):
    # Members Metrics
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='active').count()
    inactive_members = Member.objects.filter(status='inactive').count()
    frozen_members = Member.objects.filter(status='frozen').count()
    
    # Staff counts
    total_trainers = Trainer.objects.count()
    
    # Today checkins
    today = datetime.date.today()
    today_checkins = Attendance.objects.filter(date=today, status='present').count()
    
    # Financial metrics
    total_payments_count = Payment.objects.count()
    ytd_revenue = Payment.objects.filter(payment_date__year=today.year, payment_status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_revenue = Payment.objects.filter(payment_status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Membership Plans breakdown
    plans_distribution = []
    plans = MembershipPlan.objects.all()
    for plan in plans:
        count = plan.memberships.filter(status='active').count()
        plans_distribution.append({
            'plan_name': plan.name,
            'count': count,
        })
        
    context = {
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'frozen_members': frozen_members,
        'total_trainers': total_trainers,
        'today_checkins': today_checkins,
        'total_payments_count': total_payments_count,
        'ytd_revenue': ytd_revenue,
        'pending_revenue': pending_revenue,
        'plans_distribution': plans_distribution,
        'year': today.year,
    }
    return render(request, 'reports/index.html', context)
