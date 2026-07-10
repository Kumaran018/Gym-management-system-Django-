from django.db import models
from apps.members.models import Member
from django.utils import timezone

class MembershipPlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField(help_text="Duration in months")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Membership(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('frozen', 'Frozen'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='memberships')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.RESTRICT, related_name='memberships')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    paid_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(default=timezone.now)

    def is_current_active(self):
        today = timezone.now().date()
        return self.status == 'active' and self.start_date <= today <= self.end_date

    def __str__(self):
        return f"{self.member} - {self.plan.name} ({self.status})"
