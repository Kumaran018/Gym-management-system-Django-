from django import forms
from apps.authentication.models import CustomUser
from .models import Member

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MemberForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Residential Address'}))
    medical_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'E.g., Allergies, Heart issues, none'}))
    emergency_contact_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}))
    emergency_contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Phone'}))

    class Meta:
        model = Member
        fields = ['gender', 'date_of_birth', 'address', 'emergency_contact_name', 'emergency_contact_phone', 'medical_notes', 'status', 'assigned_trainer']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_trainer': forms.Select(attrs={'class': 'form-select'}),
        }
