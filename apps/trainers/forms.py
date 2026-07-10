from django import forms
from apps.authentication.models import CustomUser
from .models import Trainer

class TrainerUserForm(forms.ModelForm):
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

class TrainerForm(forms.ModelForm):
    availability = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'E.g., Mon-Fri: 6:00 AM - 12:00 PM'}))

    class Meta:
        model = Trainer
        fields = ['specialization', 'salary', 'experience_years', 'availability']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g. Strength, Yoga, Cardio'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Salary'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
        }
