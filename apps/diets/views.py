from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.authentication.decorators import role_required
from .models import DietPlan
from .forms import DietPlanForm

@login_required
def diet_list(request):
    user = request.user
    
    # Filter views based on roles
    if user.role == 'member':
        # Members only see their own diets
        diet_plans = DietPlan.objects.filter(member__user=user).select_related('trainer__user').order_by('-start_date')
    elif user.role == 'trainer':
        # Trainers see diets they created/assigned
        diet_plans = DietPlan.objects.filter(trainer__user=user).select_related('member__user').order_by('-start_date')
    else:
        # Admins/Receptionists see all
        diet_plans = DietPlan.objects.all().select_related('member__user', 'trainer__user').order_by('-start_date')
        
    return render(request, 'diets/list.html', {'diet_plans': diet_plans})

@login_required
@role_required(['admin', 'trainer'])
def diet_add(request):
    if request.method == 'POST':
        form = DietPlanForm(request.POST)
        if form.is_valid():
            diet_plan = form.save()
            messages.success(request, f"Diet Plan for {diet_plan.member} was successfully created!")
            return redirect('diets:diet_list')
    else:
        form = DietPlanForm()
        
    return render(request, 'diets/form.html', {'form': form, 'action': 'Add'})

@login_required
@role_required(['admin', 'trainer'])
def diet_edit(request, pk):
    diet_plan = get_object_or_404(DietPlan, pk=pk)
    
    if request.method == 'POST':
        form = DietPlanForm(request.POST, instance=diet_plan)
        if form.is_valid():
            form.save()
            messages.success(request, f"Diet Plan for {diet_plan.member} was successfully updated!")
            return redirect('diets:diet_list')
    else:
        form = DietPlanForm(instance=diet_plan)
        
    return render(request, 'diets/form.html', {'form': form, 'action': 'Edit'})

@login_required
@role_required(['admin', 'trainer'])
def diet_delete(request, pk):
    diet_plan = get_object_or_404(DietPlan, pk=pk)
    if request.method == 'POST':
        diet_plan.delete()
        messages.success(request, "Diet Program deleted successfully.")
        return redirect('diets:diet_list')
    return render(request, 'diets/confirm_delete.html', {'diet_plan': diet_plan})
