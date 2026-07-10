from django import forms
from django.forms import inlineformset_factory
from .models import WorkoutPlan, Exercise

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['member', 'trainer', 'start_date', 'end_date', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'trainer': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional coaching tips...'}),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'category', 'sets', 'reps', 'weight_kg', 'duration_minutes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Exercise Name'}),
            'category': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Sets'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Reps'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Weight (kg)'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Min'}),
        }

# Inline formset to add/edit exercises along with WorkoutPlan
ExerciseFormSet = inlineformset_factory(
    WorkoutPlan, 
    Exercise, 
    form=ExerciseForm, 
    extra=3, 
    can_delete=True
)
