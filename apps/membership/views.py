from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
import datetime
from apps.authentication.decorators import role_required
from apps.payments.models import Payment
from .models import MembershipPlan, Membership
from .forms import MembershipPlanForm

@login_required
def plan_list(request):
    plans = MembershipPlan.objects.all().order_by('-price')
    return render(request, 'membership/plan_list.html', {'plans': plans})

@login_required
@role_required(['admin'])
def plan_add(request):
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            plan = form.save()
            messages.success(request, f"Membership Plan '{plan.name}' created successfully!")
            return redirect('membership:plan_list')
    else:
        form = MembershipPlanForm()
    return render(request, 'membership/plan_form.html', {'form': form, 'action': 'Add'})

@login_required
@role_required(['admin'])
def plan_edit(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f"Membership Plan '{plan.name}' updated successfully!")
            return redirect('membership:plan_list')
    else:
        form = MembershipPlanForm(instance=plan)
    return render(request, 'membership/plan_form.html', {'form': form, 'action': 'Edit'})

@login_required
@role_required(['admin'])
def plan_delete(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Membership Plan deleted successfully.")
        return redirect('membership:plan_list')
    return render(request, 'membership/plan_confirm_delete.html', {'plan': plan})

@login_required
@role_required(['admin'])
def plan_toggle(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    plan.is_active = not plan.is_active
    plan.save()
    status_str = "activated" if plan.is_active else "deactivated"
    messages.success(request, f"Membership Plan '{plan.name}' has been {status_str}.")
    return redirect('membership:plan_list')

@login_required
def member_plan_list(request):
    user = request.user
    if user.role != 'member':
        messages.error(request, "Access restricted to gym members.")
        return redirect('/')

    member = user.member_profile
    today = timezone.now().date()
    
    # Check for plan purchase action
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = get_object_or_404(MembershipPlan, pk=plan_id, is_active=True)
        
        try:
            with transaction.atomic():
                # Deactivate current active memberships
                member.memberships.filter(status='active').update(status='expired')
                
                # Create new Membership
                start_date = today
                end_date = today + datetime.timedelta(days=30 * plan.duration_months)
                
                membership = Membership.objects.create(
                    member=member,
                    plan=plan,
                    start_date=start_date,
                    end_date=end_date,
                    paid_price=plan.price,
                    status='active'
                )
                
                # Create associated Payment
                Payment.objects.create(
                    member=member,
                    membership=membership,
                    amount=plan.price,
                    payment_method='online',
                    payment_status='paid'
                )
                
                messages.success(request, f"Successfully subscribed to plan '{plan.name}'! Your active membership is set until {end_date.strftime('%b %d, %Y')}.")
                return redirect('membership:member_plan_list')
        except Exception as e:
            messages.error(request, f"Subscription failed: {str(e)}")

    # Query member's active membership
    current_membership = member.memberships.filter(status='active').first()
    membership_history = member.memberships.all().order_by('-created_at')
    
    # Fetch available plan options
    available_plans = MembershipPlan.objects.filter(is_active=True).order_by('price')

    context = {
        'current_membership': current_membership,
        'membership_history': membership_history,
        'available_plans': available_plans,
    }
    return render(request, 'membership/member_plans.html', context)

