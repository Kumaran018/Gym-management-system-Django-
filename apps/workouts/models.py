from django.db import models
from apps.members.models import Member
from apps.trainers.models import Trainer
from django.utils import timezone

class WorkoutPlan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='workout_plans')
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workout_plans')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Workout Plan for {self.member} (Starts: {self.start_date})"

class Exercise(models.Model):
    CATEGORY_CHOICES = (
        ('cardio', 'Cardio'),
        ('strength', 'Strength / Weight Training'),
        ('flexibility', 'Flexibility / Stretching'),
        ('balance', 'Balance & Core'),
    )

    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='strength')
    sets = models.IntegerField(default=3)
    reps = models.IntegerField(blank=True, null=True, help_text="Number of reps per set")
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Target weight in kg")
    duration_minutes = models.IntegerField(blank=True, null=True, help_text="Target duration for cardio exercises")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
