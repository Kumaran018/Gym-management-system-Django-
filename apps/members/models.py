from django.db import models
from django.conf import settings
from django.utils import timezone

class Member(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('frozen', 'Frozen'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile')
    member_id = models.CharField(max_length=20, unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    medical_notes = models.TextField(blank=True, null=True)
    join_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    assigned_trainer = models.ForeignKey('trainers.Trainer', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_members')

    def save(self, *args, **kwargs):
        if not self.member_id:
            year = self.join_date.year if self.join_date else timezone.now().year
            prefix = f"GYM-{year}-"
            last_member = Member.objects.filter(member_id__startswith=prefix).order_by('-member_id').first()
            if last_member:
                try:
                    last_num = int(last_member.member_id.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            self.member_id = f"{prefix}{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.member_id})"

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.models import Notification

@receiver(post_save, sender=Member)
def create_member_welcome_notification(sender, instance, created, **kwargs):
    if created:
        # Member onboarding notice
        Notification.objects.create(
            user=instance.user,
            title="Welcome to Muscle Fit Gym! 🏋️‍♂️",
            message=f"Hi {instance.user.first_name or instance.user.username}, welcome to Muscle Fit Gym! Your new Member ID is {instance.member_id}. Check out your Dashboard to view your active diet plans and workout programs.",
            notification_type='welcome'
        )
        
        # System alert to Admins
        try:
            from apps.authentication.models import CustomUser
            from django.db.models import Q
            admins = CustomUser.objects.filter(Q(role='admin') | Q(is_superuser=True))
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    title="New Registration Logged! 👤",
                    message=f"New member registered: {instance.user.get_full_name() or instance.user.username} (ID: {instance.member_id}).",
                    notification_type='general'
                )
        except Exception:
            pass


