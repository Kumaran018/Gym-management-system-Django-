from django.db import models
from apps.members.models import Member
from apps.membership.models import Membership
from django.utils import timezone

class Payment(models.Model):
    METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('online', 'Online Payment'),
    )

    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    invoice_number = models.CharField(max_length=30, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='paid')
    payment_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = timezone.now().year
            prefix = f"INV-{year}-"
            last_payment = Payment.objects.filter(invoice_number__startswith=prefix).order_by('-invoice_number').first()
            if last_payment:
                try:
                    last_num = int(last_payment.invoice_number.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            self.invoice_number = f"{prefix}{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.member} (₹{self.amount})"

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.models import Notification

@receiver(post_save, sender=Payment)
def create_payment_notification(sender, instance, created, **kwargs):
    if created:
        # Notice to the member
        Notification.objects.create(
            user=instance.member.user,
            title="Payment Recorded Successfully! 💳",
            message=f"Hello, a payment of ₹{instance.amount} was recorded successfully. Invoice: {instance.invoice_number}, Status: {instance.get_payment_status_display()}.",
            notification_type='payment'
        )
        
        # System alert to Admins
        try:
            from apps.authentication.models import CustomUser
            from django.db.models import Q
            admins = CustomUser.objects.filter(Q(role='admin') | Q(is_superuser=True))
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    title="New Payment Received! 💰",
                    message=f"A payment of ₹{instance.amount} has been collected from {instance.member.user.get_full_name()} (Invoice: {instance.invoice_number}).",
                    notification_type='payment'
                )
        except Exception:
            pass


