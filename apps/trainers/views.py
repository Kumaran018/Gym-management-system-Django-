from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.members.models import Member
from .models import Trainer
from .forms import TrainerUserForm, TrainerForm

@login_required
def trainer_list(request):
    queryset = Trainer.objects.select_related('user').all()

    # Search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            specialization__icontains=search_query) | queryset.filter(
            user__first_name__icontains=search_query) | queryset.filter(
            user__last_name__icontains=search_query)

    context = {
        'trainers': queryset,
        'search_query': search_query,
    }
    return render(request, 'trainers/list.html', context)

@login_required
@role_required(['admin'])
def trainer_add(request):
    if request.method == 'POST':
        user_form = TrainerUserForm(request.POST, request.FILES)
        trainer_form = TrainerForm(request.POST)
        password = request.POST.get('password', 'trainer123')
        
        if user_form.is_valid() and trainer_form.is_valid():
            try:
                with transaction.atomic():
                    # Create CustomUser
                    user = user_form.save(commit=False)
                    user.role = 'trainer'
                    user.set_password(password)
                    user.save()

                    # Create Trainer Profile
                    trainer = trainer_form.save(commit=False)
                    trainer.user = user
                    trainer.save()

                    messages.success(request, f"Trainer {user.get_full_name()} was successfully registered!")
                    return redirect('trainers:list')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        user_form = TrainerUserForm()
        trainer_form = TrainerForm()

    return render(request, 'trainers/form.html', {
        'user_form': user_form,
        'trainer_form': trainer_form,
        'action': 'Add',
    })

@login_required
@role_required(['admin'])
def trainer_edit(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    user = trainer.user

    if request.method == 'POST':
        user_form = TrainerUserForm(request.POST, request.FILES, instance=user)
        trainer_form = TrainerForm(request.POST, instance=trainer)

        if user_form.is_valid() and trainer_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    trainer_form.save()
                    messages.success(request, f"Trainer profile for {user.get_full_name()} was successfully updated!")
                    return redirect('trainers:list')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        user_form = TrainerUserForm(instance=user)
        trainer_form = TrainerForm(instance=trainer)

    return render(request, 'trainers/form.html', {
        'user_form': user_form,
        'trainer_form': trainer_form,
        'action': 'Edit',
    })

@login_required
@role_required(['admin'])
def trainer_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    user = trainer.user

    if request.method == 'POST':
        user.delete() # Deletes user and cascades Trainer profile
        messages.success(request, f"Trainer {user.get_full_name()} was successfully deleted.")
        return redirect('trainers:list')

    return render(request, 'trainers/confirm_delete.html', {'trainer': trainer})

@login_required
@role_required(['admin', 'receptionist', 'trainer'])
def trainer_members(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    
    if request.method == 'POST':
        # Assign members action
        member_ids = request.POST.getlist('assigned_members_list')
        
        try:
            with transaction.atomic():
                # Unassign all members currently assigned to this trainer first
                trainer.assigned_members.all().update(assigned_trainer=None)
                
                # Assign selected members
                if member_ids:
                    Member.objects.filter(pk__in=member_ids).update(assigned_trainer=trainer)
                
                messages.success(request, "Trainer assignments updated successfully!")
                return redirect('trainers:members', pk=trainer.pk)
        except Exception as e:
            messages.error(request, f"Failed to assign members: {str(e)}")

    # Fetch currently assigned members
    assigned_members = trainer.assigned_members.all().select_related('user')
    
    # Fetch all members to support selection
    all_members = Member.objects.all().select_related('user')

    context = {
        'trainer': trainer,
        'assigned_members': assigned_members,
        'all_members': all_members,
    }
    return render(request, 'trainers/members.html', context)
