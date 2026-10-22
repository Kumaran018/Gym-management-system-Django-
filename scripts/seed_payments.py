import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
import django
django.setup()

from datetime import datetime, date, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.authentication.models import CustomUser
from apps.members.models import Member
from apps.membership.models import Membership, MembershipPlan
from apps.payments.models import Payment
from apps.attendance.models import Attendance

def seed_payments_and_data():
    print("--- Seeding Payments, Memberships, & Attendance ---")

    members = {m.user.username: m for m in Member.objects.all()}
    print("Members found:", list(members.keys()))

    # Ensure membership plans exist
    plan_annual, _ = MembershipPlan.objects.get_or_create(
        name="Annual VIP All-Access",
        defaults={
            "duration_months": 12,
            "price": Decimal("12000.00"),
            "description": "Full access to gym, sauna, personal trainer, and diet consultations.",
            "is_active": True
        }
    )
    plan_quarterly, _ = MembershipPlan.objects.get_or_create(
        name="Quarterly Pro Strength",
        defaults={
            "duration_months": 3,
            "price": Decimal("4500.00"),
            "description": "3-month complete access to cardio and weight training facilities.",
            "is_active": True
        }
    )
    plan_monthly, _ = MembershipPlan.objects.get_or_create(
        name="Monthly Standard Flex",
        defaults={
            "duration_months": 1,
            "price": Decimal("2000.00"),
            "description": "Monthly gym access with flexible renewal.",
            "is_active": True
        }
    )

    # Clean existing payments to establish clean realistic ledger
    Payment.objects.all().delete()
    print("Reset previous payment ledger.")

    now = timezone.now()

    payment_specs = [
        # 1. kumaran_18 (Kumaran RP)
        {
            "member_username": "kumaran_18",
            "plan": plan_annual,
            "items": [
                {
                    "amount": Decimal("12000.00"),
                    "method": "upi",
                    "status": "paid",
                    "days_ago": 15,
                    "invoice": "INV-2026-0001",
                },
                {
                    "amount": Decimal("3500.00"),
                    "method": "card",
                    "status": "paid",
                    "days_ago": 8,
                    "invoice": "INV-2026-0002",
                },
                {
                    "amount": Decimal("1250.00"),
                    "method": "online",
                    "status": "paid",
                    "days_ago": 2,
                    "invoice": "INV-2026-0003",
                }
            ]
        },
        # 2. Kumaran_10 (Kumaran R P)
        {
            "member_username": "Kumaran_10",
            "plan": plan_quarterly,
            "items": [
                {
                    "amount": Decimal("4500.00"),
                    "method": "upi",
                    "status": "paid",
                    "days_ago": 10,
                    "invoice": "INV-2026-0004",
                },
                {
                    "amount": Decimal("1500.00"),
                    "method": "card",
                    "status": "paid",
                    "days_ago": 4,
                    "invoice": "INV-2026-0005",
                }
            ]
        },
        # 3. kumaran018 (kumaran R P)
        {
            "member_username": "kumaran018",
            "plan": plan_monthly,
            "items": [
                {
                    "amount": Decimal("2000.00"),
                    "method": "upi",
                    "status": "paid",
                    "days_ago": 12,
                    "invoice": "INV-2026-0006",
                },
                {
                    "amount": Decimal("850.00"),
                    "method": "cash",
                    "status": "paid",
                    "days_ago": 3,
                    "invoice": "INV-2026-0007",
                }
            ]
        },
        # 4. member1 (Alice Smith)
        {
            "member_username": "member1",
            "plan": plan_quarterly,
            "items": [
                {
                    "amount": Decimal("4500.00"),
                    "method": "card",
                    "status": "paid",
                    "days_ago": 20,
                    "invoice": "INV-2026-0008",
                },
                {
                    "amount": Decimal("950.00"),
                    "method": "upi",
                    "status": "paid",
                    "days_ago": 5,
                    "invoice": "INV-2026-0009",
                }
            ]
        }
    ]

    for spec in payment_specs:
        m = members.get(spec["member_username"])
        if not m:
            print(f"Skipping {spec['member_username']} - not found")
            continue

        # Ensure active Membership exists for member
        mem_obj, _ = Membership.objects.get_or_create(
            member=m,
            status='active',
            defaults={
                "plan": spec["plan"],
                "start_date": date.today() - timedelta(days=30),
                "end_date": date.today() + timedelta(days=90),
                "paid_price": spec["plan"].price
            }
        )

        for item in spec["items"]:
            pay_time = now - timedelta(days=item["days_ago"], hours=item["days_ago"]*2)
            p = Payment(
                member=m,
                membership=mem_obj,
                invoice_number=item["invoice"],
                amount=item["amount"],
                payment_method=item["method"],
                payment_status=item["status"],
                payment_date=pay_time
            )
            p.save()
            print(f"Recorded Payment {p.invoice_number} (INR {p.amount}) for {m.user.username}")

        # Also ensure attendance records exist for the member
        for days_back in range(1, 6):
            att_date = date.today() - timedelta(days=days_back)
            Attendance.objects.get_or_create(
                member=m,
                date=att_date,
                defaults={
                    "check_in_time": datetime.strptime("07:30:00", "%H:%M:%S").time(),
                    "check_out_time": datetime.strptime("09:00:00", "%H:%M:%S").time(),
                    "status": "present"
                }
            )

    print("--- Done Seeding Payments, Memberships & Attendance Successfully! ---")

if __name__ == '__main__':
    seed_payments_and_data()
