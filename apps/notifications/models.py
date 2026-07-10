from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    TYPE_CHOICES = (
        ('expiry', 'Membership Expiry Warning'),
        ('payment', 'Payment Reminder/Invoice Receipt'),
        ('welcome', 'Welcome Onboarding Alert'),
        ('birthday', 'Birthday Wishes'),
        ('trainer', 'Trainer Assignment notification'),
        ('general', 'General Announcement'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification to {self.user.username} - {self.title}"
