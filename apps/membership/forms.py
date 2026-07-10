from django import forms
from .models import MembershipPlan

class MembershipPlanForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter plan description...'}))

    class Meta:
        model = MembershipPlan
        fields = ['name', 'price', 'duration_months', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Monthly Basic, Yearly Premium'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Subscription Price ($)'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (Months)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
