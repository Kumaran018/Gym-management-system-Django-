import os
import sys
import django

# Add project directory to PYTHONPATH
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
django.setup()

from django.contrib.auth.models import Group
from apps.authentication.models import CustomUser
from apps.trainers.models import Trainer
from apps.membership.models import MembershipPlan

# Ensure Groups exist
admin_group, _ = Group.objects.get_or_create(name='admin')
receptionist_group, _ = Group.objects.get_or_create(name='receptionist')
trainer_group, _ = Group.objects.get_or_create(name='trainer')
member_group, _ = Group.objects.get_or_create(name='member')

print("Seeding Plans...")
plans = [
    {
        "name": "Monthly Standard",
        "price": 50.00,
        "duration_months": 1,
        "description": "Standard monthly package with cardio & gym floor access.",
        "is_active": True
    },
    {
        "name": "Quarterly Special",
        "price": 130.00,
        "duration_months": 3,
        "description": "Discounted quarterly access with 2 free trainer sessions.",
        "is_active": True
    },
    {
        "name": "Yearly Gold VIP",
        "price": 450.00,
        "duration_months": 12,
        "description": "VIP membership with unlimited locker access, trainer coaching, and nutrition plans.",
        "is_active": True
    }
]

for p in plans:
    plan, created = MembershipPlan.objects.get_or_create(
        name=p["name"],
        defaults={
            "price": p["price"],
            "duration_months": p["duration_months"],
            "description": p["description"],
            "is_active": p["is_active"]
        }
    )
    if created:
        print(f"Created Plan: {plan.name}")

print("Seeding Trainers...")
trainers_data = [
    {
        "username": "trainer2",
        "first_name": "Mike",
        "last_name": "Tyson",
        "email": "mike@example.com",
        "specialization": "Boxing & Strength Training",
        "salary": 4000.00,
        "experience": 10,
        "hours": "Mon-Fri: 6:00 AM - 12:00 PM"
    },
    {
        "username": "trainer3",
        "first_name": "Serena",
        "last_name": "Williams",
        "email": "serena@example.com",
        "specialization": "Cardio & Stamina Conditioning",
        "salary": 3800.00,
        "experience": 8,
        "hours": "Mon-Sat: 1:00 PM - 7:00 PM"
    },
    {
        "username": "trainer4",
        "first_name": "Arnold",
        "last_name": "Schwarzenegger",
        "email": "arnold@example.com",
        "specialization": "Hypertrophy & Bodybuilding",
        "salary": 5000.00,
        "experience": 15,
        "hours": "Mon-Fri: 2:00 PM - 10:00 PM"
    }
]

for t in trainers_data:
    user, created = CustomUser.objects.get_or_create(
        username=t["username"],
        defaults={
            "first_name": t["first_name"],
            "last_name": t["last_name"],
            "email": t["email"],
            "role": "trainer"
        }
    )
    if created:
        user.set_password("trainer123")
        user.save()
        user.groups.add(trainer_group)
        
        Trainer.objects.create(
            user=user,
            specialization=t["specialization"],
            salary=t["salary"],
            experience_years=t["experience"],
            availability=t["hours"]
        )
        print(f"Created Trainer: {user.get_full_name()}")

print("Seeding Receptionists...")
receptionists_data = [
    {
        "username": "receptionist2",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@example.com",
    },
    {
        "username": "receptionist3",
        "first_name": "Emma",
        "last_name": "Watson",
        "email": "emma@example.com",
    }
]

for r in receptionists_data:
    user, created = CustomUser.objects.get_or_create(
        username=r["username"],
        defaults={
            "first_name": r["first_name"],
            "last_name": r["last_name"],
            "email": r["email"],
            "role": "receptionist"
        }
    )
    if created:
        user.set_password("receptionist123")
        user.save()
        user.groups.add(receptionist_group)
        print(f"Created Receptionist: {user.get_full_name()}")

print("Seeding finished successfully!")
