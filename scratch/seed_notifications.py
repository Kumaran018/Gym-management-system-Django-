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

print("Seeding notifications...")
users = CustomUser.objects.all()
for user in users:
    if user.role == 'member':
        # Welcome
        Notification.objects.get_or_create(
            user=user,
            title="Welcome to Muscle Fit Gym! 🏋️‍♂️",
            defaults={
                "message": f"Hi {user.first_name or user.username}, welcome to Muscle Fit Gym! Check out your Dashboard to view your active diet plans and workout programs.",
                "notification_type": "welcome"
            }
        )
        # Payment
        Notification.objects.get_or_create(
            user=user,
            title="Subscription Active! 💳",
            defaults={
                "message": "Your membership subscription has been successfully activated. Access to all gym floor spaces and accessories is enabled.",
                "notification_type": "payment"
            }
        )
        # Plan
        Notification.objects.get_or_create(
            user=user,
            title="Diet Plan Assigned 🍎",
            defaults={
                "message": "A personalized nutrition diet plan macro schedule has been assigned to you. Go to the Nutrition Diet tab to view.",
                "notification_type": "general"
            }
        )
print("Seeding complete!")
