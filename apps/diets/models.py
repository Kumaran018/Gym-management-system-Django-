from django.db import models
from apps.members.models import Member
from apps.trainers.models import Trainer
from django.utils import timezone

class DietPlan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='diet_plans')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_diet_plans')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    daily_calories = models.IntegerField(help_text="Target daily calories (kcal)")
    protein_g = models.IntegerField(help_text="Target protein in grams")
    carbs_g = models.IntegerField(help_text="Target carbohydrates in grams")
    fat_g = models.IntegerField(help_text="Target fats in grams")
    meal_schedule = models.JSONField(
        default=dict, 
        help_text="Meal schedules structured as JSON, e.g., {'Breakfast': 'Eggs and oats', 'Lunch': 'Chicken and rice'}"
    )

    def __str__(self):
        return f"Diet Plan for {self.member} (Starts: {self.start_date})"
