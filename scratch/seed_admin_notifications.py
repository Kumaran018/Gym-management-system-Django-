import os
import sys
import django

# Add project directory to PYTHONPATH
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
django.setup()

from apps.authentication.models import CustomUser
from apps.notifications.models import Notification

print("Seeding admin notifications...")
admins = CustomUser.objects.filter(role='admin') | CustomUser.objects.filter(is_superuser=True)
for admin in admins:
    # Notification 1: Member signup
    Notification.objects.get_or_create(
        user=admin,
        title="New Registration Logged! 👤",
        defaults={
            "message": "New member registered: Kumaran RP (ID: GYM-2026-0001). Welcome onboarding alert has been sent.",
            "notification_type": "general"
        }
    )
    # Notification 2: Payment collected
    Notification.objects.get_or_create(
        user=admin,
        title="New Payment Received! 💰",
        defaults={
            "message": "A payment of ₹10,000.00 has been collected from Kumaran RP (Invoice: INV-2026-0001) for Yearly Gold VIP.",
            "notification_type": "payment"
        }
    )
    # Notification 3: Trainer assigned
    Notification.objects.get_or_create(
        user=admin,
        title="Trainer Assignment Alert 🏋️‍♂️",
        defaults={
            "message": "Trainer Mike Tyson has been assigned to client Kumaran RP.",
            "notification_type": "trainer"
        }
    )
print("Seeding complete!")
