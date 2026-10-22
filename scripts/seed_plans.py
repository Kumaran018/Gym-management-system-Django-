import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
import django
django.setup()

from datetime import date, timedelta
from apps.authentication.models import CustomUser
from apps.members.models import Member
from apps.trainers.models import Trainer
from apps.workouts.models import WorkoutPlan, Exercise
from apps.diets.models import DietPlan

def seed_data():
    print("--- Seeding Workouts & Nutrition Plans ---")
    
    # Fetch members
    members = {m.user.username: m for m in Member.objects.all()}
    print("Found members:", list(members.keys()))
    
    # Fetch trainers
    trainers = list(Trainer.objects.all())
    print("Found trainers:", len(trainers))
    t_arnold = Trainer.objects.filter(user__first_name__icontains='Arnold').first() or (trainers[2] if len(trainers) > 2 else trainers[0])
    t_serena = Trainer.objects.filter(user__first_name__icontains='Serena').first() or (trainers[1] if len(trainers) > 1 else trainers[0])
    t_john = Trainer.objects.filter(user__first_name__icontains='John').first() or trainers[0]

    # Clean existing workout and diet plans to prevent duplicates
    WorkoutPlan.objects.all().delete()
    DietPlan.objects.all().delete()
    print("Cleared existing plans.")

    today = date.today()
    in_3_months = today + timedelta(days=90)

    # 1. Workout Plans and Exercises
    workout_configs = [
        {
            "member_username": "kumaran_18",
            "trainer": t_arnold,
            "notes": "Hypertrophy Push-Pull-Legs Split. Focus on progressive overload, 2-3 min rest on compounds, 2-second eccentric phase. Maintain 3.5L hydration daily.",
            "exercises": [
                {"name": "Barbell Bench Press", "category": "strength", "sets": 4, "reps": 8, "weight_kg": 85.0, "duration_minutes": None},
                {"name": "Incline Dumbbell Press", "category": "strength", "sets": 4, "reps": 10, "weight_kg": 32.0, "duration_minutes": None},
                {"name": "Standing Barbell Overhead Press", "category": "strength", "sets": 3, "reps": 8, "weight_kg": 55.0, "duration_minutes": None},
                {"name": "Barbell Back Squats", "category": "strength", "sets": 4, "reps": 8, "weight_kg": 110.0, "duration_minutes": None},
                {"name": "Romanian Deadlift", "category": "strength", "sets": 3, "reps": 10, "weight_kg": 90.0, "duration_minutes": None},
                {"name": "Weighted Pull-ups", "category": "strength", "sets": 4, "reps": 8, "weight_kg": 15.0, "duration_minutes": None},
                {"name": "Cable Lateral Raises", "category": "strength", "sets": 4, "reps": 15, "weight_kg": 14.0, "duration_minutes": None},
                {"name": "HIIT Treadmill Sprints", "category": "cardio", "sets": 6, "reps": None, "weight_kg": None, "duration_minutes": 20},
            ]
        },
        {
            "member_username": "Kumaran_10",
            "trainer": t_john,
            "notes": "Functional Strength & Explosive Athletic Power. Prioritize core stability, full hip hinge on deadlifts, and controlled tempo.",
            "exercises": [
                {"name": "Trap Bar Deadlift", "category": "strength", "sets": 4, "reps": 6, "weight_kg": 120.0, "duration_minutes": None},
                {"name": "Front Squat", "category": "strength", "sets": 4, "reps": 8, "weight_kg": 80.0, "duration_minutes": None},
                {"name": "Dumbbell Renegade Rows", "category": "strength", "sets": 3, "reps": 12, "weight_kg": 24.0, "duration_minutes": None},
                {"name": "Kettlebell Clean & Press", "category": "strength", "sets": 4, "reps": 10, "weight_kg": 20.0, "duration_minutes": None},
                {"name": "Hanging Toes-To-Bar", "category": "balance", "sets": 4, "reps": 12, "weight_kg": None, "duration_minutes": None},
                {"name": "Rowing Machine Intervals", "category": "cardio", "sets": 4, "reps": None, "weight_kg": None, "duration_minutes": 15},
            ]
        },
        {
            "member_username": "kumaran018",
            "trainer": t_serena,
            "notes": "Lean Shred & Stamina Conditioning. Short rest intervals (45-60s max). Combine strength supersets with high-intensity cardio finish.",
            "exercises": [
                {"name": "Treadmill Incline Intervals", "category": "cardio", "sets": 1, "reps": None, "weight_kg": None, "duration_minutes": 25},
                {"name": "Plyometric Box Jumps", "category": "cardio", "sets": 4, "reps": 15, "weight_kg": None, "duration_minutes": None},
                {"name": "Bulgarian Split Squats", "category": "strength", "sets": 3, "reps": 12, "weight_kg": 18.0, "duration_minutes": None},
                {"name": "Cable Lat Pulldown", "category": "strength", "sets": 4, "reps": 12, "weight_kg": 65.0, "duration_minutes": None},
                {"name": "Cable Face Pulls", "category": "strength", "sets": 4, "reps": 15, "weight_kg": 25.0, "duration_minutes": None},
                {"name": "Core Plank Hold & Hollow Body", "category": "balance", "sets": 4, "reps": None, "weight_kg": None, "duration_minutes": 2},
            ]
        },
        {
            "member_username": "member1",
            "trainer": t_john,
            "notes": "Full-Body Muscle Definition & Conditioning. Focus on form, mind-muscle connection, and pre-workout mobility warmup.",
            "exercises": [
                {"name": "Kettlebell Goblet Squats", "category": "strength", "sets": 3, "reps": 12, "weight_kg": 16.0, "duration_minutes": None},
                {"name": "Dumbbell Flat Chest Press", "category": "strength", "sets": 3, "reps": 10, "weight_kg": 14.0, "duration_minutes": None},
                {"name": "Seated Cable Rows", "category": "strength", "sets": 3, "reps": 12, "weight_kg": 35.0, "duration_minutes": None},
                {"name": "Core Abdominal Plank", "category": "balance", "sets": 3, "reps": None, "weight_kg": None, "duration_minutes": 1},
                {"name": "Elliptical Zone 2 Stamina", "category": "cardio", "sets": 1, "reps": None, "weight_kg": None, "duration_minutes": 20},
            ]
        }
    ]

    for cfg in workout_configs:
        m = members.get(cfg["member_username"])
        if not m:
            print(f"Skipping workout for {cfg['member_username']} (not found)")
            continue
        wp = WorkoutPlan.objects.create(
            member=m,
            trainer=cfg["trainer"],
            start_date=today,
            end_date=in_3_months,
            notes=cfg["notes"]
        )
        for ex in cfg["exercises"]:
            Exercise.objects.create(
                workout_plan=wp,
                name=ex["name"],
                category=ex["category"],
                sets=ex["sets"],
                reps=ex["reps"],
                weight_kg=ex["weight_kg"],
                duration_minutes=ex["duration_minutes"]
            )
        print(f"Created WorkoutPlan id={wp.id} for {m.user.username} with {len(cfg['exercises'])} exercises.")

    # 2. Nutrition / Diet Plans
    diet_configs = [
        {
            "member_username": "kumaran_18",
            "trainer": t_arnold,
            "daily_calories": 2850,
            "protein_g": 195,
            "carbs_g": 330,
            "fat_g": 75,
            "schedule": (
                "Breakfast (8:00 AM): 4 whole eggs scrambled, 100g rolled oats with 1 tbsp peanut butter and berries.\n"
                "Mid-Morning (11:00 AM): Whey isolate shake (30g protein), 1 ripe banana, 30g raw almonds.\n"
                "Lunch (1:30 PM): 220g grilled chicken breast, 1.5 cups steamed basmati rice, steamed broccoli & 1 tbsp olive oil.\n"
                "Pre-Workout (4:30 PM): 3 rice cakes with natural honey + double espresso.\n"
                "Post-Workout Dinner (7:30 PM): 200g lean salmon fillet, baked sweet potato, large mixed greens with avocado.\n"
                "Before Sleep (10:00 PM): 200g Greek yogurt with chia seeds."
            )
        },
        {
            "member_username": "Kumaran_10",
            "trainer": t_serena,
            "daily_calories": 2100,
            "protein_g": 185,
            "carbs_g": 180,
            "fat_g": 55,
            "schedule": (
                "Breakfast (7:30 AM): Egg white omelette (5 whites + 1 yolk) with baby spinach, mushrooms, 1 slice whole-wheat toast.\n"
                "Mid-Morning (10:30 AM): Low-fat Greek yogurt (150g) with 1 scoop vanilla whey protein.\n"
                "Lunch (1:00 PM): 200g grilled turkey breast or extra-lean ground beef, 1 cup cooked quinoa, steamed green beans.\n"
                "Afternoon Snack (4:00 PM): Crisp green apple + 15g walnut halves.\n"
                "Dinner (7:00 PM): 220g grilled white fish (cod/tilapia), roasted asparagus and bell peppers in olive oil spray.\n"
                "Hydration: Drink minimum 4.0 Liters cold water daily."
            )
        },
        {
            "member_username": "kumaran018",
            "trainer": t_john,
            "daily_calories": 2600,
            "protein_g": 170,
            "carbs_g": 320,
            "fat_g": 70,
            "schedule": (
                "Breakfast (8:00 AM): Overnight oats with unsweetened almond milk, chia seeds, sliced bananas and chocolate whey.\n"
                "Morning Snack (11:00 AM): 2 whole grain rice cakes with almond butter and organic honey.\n"
                "Lunch (1:30 PM): 200g grilled chicken thighs (skinless), brown rice bowl with avocado, salsa, and black beans.\n"
                "Intra-Workout (5:00 PM): Essential amino acids (EAA) + electrolyte drink.\n"
                "Dinner (8:00 PM): 200g lean sirloin steak, roasted baby potatoes, grilled zucchini.\n"
                "Night (10:30 PM): Casein protein shake with unsweetened almond milk."
            )
        },
        {
            "member_username": "member1",
            "trainer": t_serena,
            "daily_calories": 1850,
            "protein_g": 145,
            "carbs_g": 175,
            "fat_g": 50,
            "schedule": (
                "Breakfast (8:00 AM): 2 poached eggs, half mashed avocado on seeded sourdough toast, cup of green tea.\n"
                "Mid-Morning (11:00 AM): Protein smoothie with spinach, blueberries, whey isolate and chia seeds.\n"
                "Lunch (1:30 PM): Grilled lemon herb chicken salad with quinoa, cherry tomatoes, cucumbers and balsamic drizzle.\n"
                "Afternoon Snack (4:30 PM): Low-fat cottage cheese with fresh strawberries.\n"
                "Dinner (7:30 PM): Baked Atlantic cod, steamed sweet potato mash and sautéed asparagus."
            )
        }
    ]

    for cfg in diet_configs:
        m = members.get(cfg["member_username"])
        if not m:
            print(f"Skipping diet for {cfg['member_username']} (not found)")
            continue
        dp = DietPlan.objects.create(
            member=m,
            trainer=cfg["trainer"],
            start_date=today,
            end_date=in_3_months,
            daily_calories=cfg["daily_calories"],
            protein_g=cfg["protein_g"],
            carbs_g=cfg["carbs_g"],
            fat_g=cfg["fat_g"],
            meal_schedule={"schedule": cfg["schedule"]}
        )
        print(f"Created DietPlan id={dp.id} for {m.user.username} ({cfg['daily_calories']} kcal).")

    print("--- Done Seeding Plans Successfully! ---")

if __name__ == '__main__':
    seed_data()
