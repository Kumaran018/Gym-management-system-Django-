from django.db import models
from django.conf import settings
from django.utils import timezone

class Trainer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer_profile')
    trainer_id = models.CharField(max_length=20, unique=True, blank=True)
    specialization = models.CharField(max_length=100)
    salary = models.DecimalField(max_length=10, max_digits=10, decimal_places=2)
    experience_years = models.IntegerField(default=0)
    availability = models.TextField(help_text="Days and timings, e.g., Mon-Fri: 6:00 AM - 12:00 PM")

    def save(self, *args, **kwargs):
        if not self.trainer_id:
            year = timezone.now().year
            prefix = f"TRN-{year}-"
            last_trainer = Trainer.objects.filter(trainer_id__startswith=prefix).order_by('-trainer_id').first()
            if last_trainer:
                try:
                    last_num = int(last_trainer.trainer_id.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            self.trainer_id = f"{prefix}{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.specialization})"
