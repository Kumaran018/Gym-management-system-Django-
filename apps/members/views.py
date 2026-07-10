from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from .models import Member
from .forms import UserForm, MemberForm

@login_required
@role_required(['admin', 'receptionist', 'trainer'])
def member_list(request):
    # Query all members with user records loaded
    queryset = Member.objects.select_related('user').all().order_by('-join_date')

    # Apply Search Filter (Search by Name, Email, Member ID, Phone)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(member_id__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__phone__icontains=search_query)
        )

    # Apply Status Filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Apply Gender Filter
    gender_filter = request.GET.get('gender', '').strip()
    if gender_filter:
        queryset = queryset.filter(gender=gender_filter)

    # Pagination (10 members per page)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'gender_filter': gender_filter,
    }
    return render(request, 'members/list.html', context)

@login_required
@role_required(['admin', 'receptionist'])
def member_add(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        member_form = MemberForm(request.POST)
        password = request.POST.get('password', 'member123') # Default password for member
        
        if user_form.is_valid() and member_form.is_valid():
            try:
                with transaction.atomic():
                    # Create custom user
                    user = user_form.save(commit=False)
                    user.role = 'member'
                    user.set_password(password)
                    user.save()
                    
                    # Associate and save member profile
                    member = member_form.save(commit=False)
                    member.user = user
                    member.save()
                    
                    messages.success(request, f"Member {user.get_full_name()} was successfully registered with ID {member.member_id}!")
                    return redirect('members:list')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        user_form = UserForm()
        member_form = MemberForm()

    return render(request, 'members/form.html', {
        'user_form': user_form,
        'member_form': member_form,
        'action': 'Add',
    })

@login_required
@role_required(['admin', 'receptionist'])
def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    user = member.user
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        member_form = MemberForm(request.POST, instance=member)
        
        if user_form.is_valid() and member_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    member_form.save()
                    messages.success(request, f"Member profile for {user.get_full_name()} was successfully updated!")
                    return redirect('members:profile', pk=member.pk)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        user_form = UserForm(instance=user)
        member_form = MemberForm(instance=member)

    return render(request, 'members/form.html', {
        'user_form': user_form,
        'member_form': member_form,
        'action': 'Edit',
    })

@login_required
@role_required(['admin']) # RESTRICT DELETIONS TO ADMIN ONLY (receptionist blocked)
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    user = member.user
    
    if request.method == 'POST':
        user.delete() # Deletes user and cascaded member profile
        messages.success(request, f"Member record with ID {member.member_id} was successfully deleted.")
        return redirect('members:list')
        
    return render(request, 'members/confirm_delete.html', {'member': member})

@login_required
def member_profile(request, pk):
    member = get_object_or_404(Member, pk=pk)
    user = request.user
    
    # SECURITY POLICY: If role is member, they can only view their own profile
    if user.role == 'member' and member.user != user:
        messages.error(request, "Access denied: You are not authorized to view this profile.")
        return redirect('dashboard:member_home')
        
    # Get associated metrics
    memberships = member.memberships.all().order_by('-created_at')
    current_membership = memberships.filter(status='active').first()
    attendances = member.attendances.all().order_by('-date')[:15]
    payments = member.payments.all().order_by('-payment_date')[:10]
    
    # Workout and diet
    workout_plan = member.workout_plans.order_by('-start_date').first()
    diet_plan = member.diet_plans.order_by('-start_date').first()

    context = {
        'member': member,
        'memberships': memberships,
        'current_membership': current_membership,
        'attendances': attendances,
        'payments': payments,
        'workout_plan': workout_plan,
        'diet_plan': diet_plan,
    }
    return render(request, 'members/profile.html', context)
