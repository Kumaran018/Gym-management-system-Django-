from django.db import models

class GymItem(models.Model):
    CATEGORY_CHOICES = (
        ('cardio', 'Cardio Equipment'),
        ('strength', 'Strength & Free Weights'),
        ('studio', 'Studio & Classes'),
        ('accessories', 'Gym Accessories'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cardio')
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.name} - {self.get_category_display()} ({self.status})"
