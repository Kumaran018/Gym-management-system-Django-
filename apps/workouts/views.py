from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.authentication.decorators import role_required
from .models import WorkoutPlan, Exercise
from .forms import WorkoutPlanForm, ExerciseFormSet

@login_required
def workout_list(request):
    user = request.user
    
    if user.role == 'member':
        # Strictly show only this particular member's workouts
        workout_plans = WorkoutPlan.objects.filter(member__user=user).select_related('trainer__user', 'member__user').order_by('-start_date')
    elif user.role == 'trainer':
        # Trainers see workouts they created/assigned
        workout_plans = WorkoutPlan.objects.filter(trainer__user=user).select_related('member__user').order_by('-start_date')
    else:
        # Admins/Staff see all
        workout_plans = WorkoutPlan.objects.all().select_related('member__user', 'trainer__user').order_by('-start_date')
        
    return render(request, 'workouts/list.html', {'workout_plans': workout_plans})

@login_required
@role_required(['admin', 'trainer'])
def workout_add(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    workout_plan = form.save()
                    formset = ExerciseFormSet(request.POST, instance=workout_plan)
                    if formset.is_valid():
                        formset.save()
                        messages.success(request, f"Workout Plan for {workout_plan.member} was successfully created!")
                        return redirect('workouts:workout_list')
            except Exception as e:
                messages.error(request, f"Error saving workout program: {str(e)}")
    else:
        form = WorkoutPlanForm()
        formset = ExerciseFormSet()
        
    return render(request, 'workouts/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Add'
    })

@login_required
@role_required(['admin', 'trainer'])
def workout_edit(request, pk):
    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
    
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, instance=workout_plan)
        formset = ExerciseFormSet(request.POST, instance=workout_plan)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    formset.save()
                    messages.success(request, f"Workout Plan for {workout_plan.member} was successfully updated!")
                    return redirect('workouts:workout_list')
            except Exception as e:
                messages.error(request, f"Error updating workout program: {str(e)}")
    else:
        form = WorkoutPlanForm(instance=workout_plan)
        formset = ExerciseFormSet(instance=workout_plan)
        
    return render(request, 'workouts/form.html', {
        'form': form,
        'formset': formset,
        'action': 'Edit'
    })

@login_required
@role_required(['admin', 'trainer'])
def workout_delete(request, pk):
    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
    if request.method == 'POST':
        workout_plan.delete()
        messages.success(request, "Workout Program deleted successfully.")
        return redirect('workouts:workout_list')
    return render(request, 'workouts/confirm_delete.html', {'workout_plan': workout_plan})
