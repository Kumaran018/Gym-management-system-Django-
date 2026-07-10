from django import forms
from .models import DietPlan
import json

class DietPlanForm(forms.ModelForm):
    meal_schedule = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Breakfast: 3 boiled eggs, oats\nLunch: Chicken breast, brown rice\nDinner: Salmon salad'}),
        help_text="Enter meals on new lines."
    )

    class Meta:
        model = DietPlan
        fields = ['member', 'trainer', 'start_date', 'end_date', 'daily_calories', 'protein_g', 'carbs_g', 'fat_g', 'meal_schedule']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'trainer': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'daily_calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target Calories (kcal)'}),
            'protein_g': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Protein (g)'}),
            'carbs_g': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carbohydrates (g)'}),
            'fat_g': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fats (g)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing plan, extract schedule from JSON dictionary
        if self.instance and self.instance.pk:
            schedule_data = self.instance.meal_schedule
            if isinstance(schedule_data, dict):
                self.initial['meal_schedule'] = schedule_data.get('schedule', '')
            else:
                self.initial['meal_schedule'] = schedule_data

    def clean_meal_schedule(self):
        schedule_text = self.cleaned_data.get('meal_schedule', '').strip()
        # Save as JSON dictionary
        return {'schedule': schedule_text}
