from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import Group
from apps.members.models import Member
from apps.authentication.decorators import role_required
from .models import CustomUser
from .forms import MemberRegistrationForm, ReceptionistUserForm

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = False
        
    def get_success_url(self):
        return '/dashboard/'

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')
        
    def post(self, request):
        logout(request)
        return redirect('/login/')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = MemberRegistrationForm()
        return render(request, 'authentication/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create CustomUser
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role='member',
                phone=form.cleaned_data['phone']
            )
            
            # 2. Add to Member Group
            member_group, _ = Group.objects.get_or_create(name='Member')
            user.groups.add(member_group)
            
            # 3. Create Member Profile
            member_profile = Member.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                address=form.cleaned_data['address'],
                emergency_contact_name=form.cleaned_data['emergency_contact_name'],
                emergency_contact_phone=form.cleaned_data['emergency_contact_phone']
            )
            
            # 4. Log User In
            login(request, user)
            return redirect('dashboard:member_home')
            
        return render(request, 'authentication/register.html', {'form': form})

@login_required
@role_required(['admin'])
def receptionist_list(request):
    receptionists = CustomUser.objects.filter(role='receptionist')
    return render(request, 'receptionists/list.html', {'receptionists': receptionists})

@login_required
@role_required(['admin'])
def receptionist_add(request):
    if request.method == 'POST':
        form = ReceptionistUserForm(request.POST, request.FILES)
        password = request.POST.get('password', 'receptionist123')
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'receptionist'
            user.set_password(password)
            user.save()
            
            # Make sure to add user to Receptionist Group
            receptionist_group, _ = Group.objects.get_or_create(name='Receptionist')
            user.groups.add(receptionist_group)
            
            messages.success(request, f"Receptionist staff {user.get_full_name()} registered successfully!")
            return redirect('authentication:receptionist_list')
    else:
        form = ReceptionistUserForm()
    return render(request, 'receptionists/form.html', {'form': form, 'action': 'Add'})

@login_required
@role_required(['admin'])
def receptionist_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, role='receptionist')
    if request.method == 'POST':
        form = ReceptionistUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Receptionist profile for {user.get_full_name()} updated!")
            return redirect('authentication:receptionist_list')
    else:
        form = ReceptionistUserForm(instance=user)
    return render(request, 'receptionists/form.html', {'form': form, 'action': 'Edit'})

@login_required
@role_required(['admin'])
def receptionist_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, role='receptionist')
    if request.method == 'POST':
        user.delete()
        messages.success(request, f"Receptionist account deleted successfully.")
        return redirect('authentication:receptionist_list')
    return render(request, 'receptionists/confirm_delete.html', {'receptionist': user})


