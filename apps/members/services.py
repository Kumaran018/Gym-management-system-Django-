from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from apps.workouts.models import WorkoutPlan, Exercise
from apps.diets.models import DietPlan
from apps.trainers.models import Trainer

def calculate_biometrics(height_cm, weight_kg, gender='M', birth_date=None):
    """
    Computes BMI, BMR (Mifflin-St Jeor), TDEE, and recommended fitness category.
    """
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    h_m = height_cm / 100.0
    bmi = round(weight_kg / (h_m * h_m), 1)

    # Estimate age
    if birth_date:
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    else:
        age = 25

    # Mifflin-St Jeor Formula
    if gender == 'F':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5

    # TDEE with moderate gym training multiplier (1.45)
    tdee = round(bmr * 1.45)

    if bmi < 18.5:
        category = "underweight"
        category_label = "Underweight & Mass Gain"
        target_calories = max(2700, tdee + 500)
        protein_g = round(weight_kg * 2.0)
        fat_g = round(weight_kg * 1.0)
    elif bmi < 25.0:
        category = "normal"
        category_label = "Normal Weight & Athletic Performance"
        target_calories = tdee + 200
        protein_g = round(weight_kg * 2.0)
        fat_g = round(weight_kg * 0.9)
    elif bmi < 30.0:
        category = "overweight"
        category_label = "Overweight & Fat Shred Recomposition"
        target_calories = max(1800, tdee - 450)
        protein_g = round(weight_kg * 2.2)
        fat_g = round(weight_kg * 0.75)
    else:
        category = "obese"
        category_label = "Obese & Joint-Safe Fat Loss"
        target_calories = max(1750, tdee - 600)
        protein_g = round(max(50, height_cm - 100) * 2.0)
        fat_g = round(weight_kg * 0.65)

    # Calculate remaining carbs
    carbs_calories = max(400, target_calories - (protein_g * 4) - (fat_g * 9))
    carbs_g = round(carbs_calories / 4)

    return {
        'bmi': bmi,
        'category': category,
        'category_label': category_label,
        'bmr': round(bmr),
        'tdee': tdee,
        'target_calories': target_calories,
        'protein_g': protein_g,
        'carbs_g': carbs_g,
        'fat_g': fat_g
    }


def assign_plans_by_biometrics(member, height_cm, weight_kg, trainer=None):
    """
    Saves height & weight on member and automatically generates personalized
    Workout and Diet plans based on scientific BMI and calorie calculations.
    """
    height_cm = Decimal(str(height_cm))
    weight_kg = Decimal(str(weight_kg))

    # Save measurements to member profile
    member.height_cm = height_cm
    member.weight_kg = weight_kg
    member.save()

    metrics = calculate_biometrics(
        height_cm=float(height_cm),
        weight_kg=float(weight_kg),
        gender=member.gender,
        birth_date=member.date_of_birth
    )

    if not trainer:
        trainer = member.assigned_trainer or Trainer.objects.first()

    today = date.today()
    in_3_months = today + timedelta(days=90)

    # Remove previous active plans for clean replacement
    member.workout_plans.all().delete()
    member.diet_plans.all().delete()

    cat = metrics['category']
    bmi = metrics['bmi']

    # 1. GENERATE WORKOUT PROGRAM
    if cat == 'underweight':
        workout_notes = (
            f"Hypertrophy Mass Builder prescribed for BMI {bmi} (Height: {height_cm}cm, Weight: {weight_kg}kg). "
            f"Focus on progressive overload on heavy compound lifts, 2-3 minutes rest between sets, and zero missed meals."
        )
        exercises_data = [
            {"name": "Barbell Back Squats", "category": "strength", "sets": 4, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 1.1, 1))), "duration_minutes": None},
            {"name": "Barbell Bench Press", "category": "strength", "sets": 4, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 0.9, 1))), "duration_minutes": None},
            {"name": "Romanian Deadlift", "category": "strength", "sets": 3, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 1.0, 1))), "duration_minutes": None},
            {"name": "Standing Overhead Press", "category": "strength", "sets": 3, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 0.6, 1))), "duration_minutes": None},
            {"name": "Bent-Over Barbell Rows", "category": "strength", "sets": 4, "reps": 10, "weight_kg": Decimal(str(round(float(weight_kg) * 0.7, 1))), "duration_minutes": None},
            {"name": "Weighted Dips", "category": "strength", "sets": 3, "reps": 10, "weight_kg": Decimal("10.00"), "duration_minutes": None},
            {"name": "Standing Dumbbell Bicep Curls", "category": "strength", "sets": 3, "reps": 12, "weight_kg": Decimal("14.00"), "duration_minutes": None},
        ]
        meal_schedule = (
            "Breakfast (8:00 AM): 4 whole eggs scrambled in butter, 100g rolled oats with whole milk, 2 tbsp peanut butter & sliced banana.\n"
            "Mid-Morning (11:00 AM): 1 scoop whey isolate + 30g raw almonds + 1 whole wheat bagel.\n"
            "Lunch (1:30 PM): 220g grilled chicken breast, 2 cups steamed basmati rice, steamed broccoli & 1 tbsp olive oil.\n"
            "Pre-Workout (4:30 PM): 3 rice cakes with organic honey + banana + black coffee.\n"
            "Post-Workout Dinner (7:30 PM): 200g lean salmon fillet or beef, large sweet potato, mixed greens with avocado.\n"
            "Bedtime (10:00 PM): 200g Greek yogurt with chia seeds and walnuts."
        )

    elif cat == 'normal':
        workout_notes = (
            f"Push-Pull-Legs Athletic Performance Split prescribed for BMI {bmi} (Height: {height_cm}cm, Weight: {weight_kg}kg). "
            f"Optimized for lean muscle hypertrophy, explosive power, and functional athletic stamina."
        )
        exercises_data = [
            {"name": "Barbell Bench Press", "category": "strength", "sets": 4, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 1.0, 1))), "duration_minutes": None},
            {"name": "Incline Dumbbell Press", "category": "strength", "sets": 4, "reps": 10, "weight_kg": Decimal("30.00"), "duration_minutes": None},
            {"name": "Barbell Back Squats", "category": "strength", "sets": 4, "reps": 8, "weight_kg": Decimal(str(round(float(weight_kg) * 1.2, 1))), "duration_minutes": None},
            {"name": "Weighted Pull-ups", "category": "strength", "sets": 4, "reps": 8, "weight_kg": Decimal("12.00"), "duration_minutes": None},
            {"name": "Cable Lateral Raises", "category": "strength", "sets": 4, "reps": 15, "weight_kg": Decimal("14.00"), "duration_minutes": None},
            {"name": "Hanging Leg Raises", "category": "balance", "sets": 4, "reps": 15, "weight_kg": None, "duration_minutes": None},
            {"name": "HIIT Treadmill Sprints", "category": "cardio", "sets": 5, "reps": None, "weight_kg": None, "duration_minutes": 15},
        ]
        meal_schedule = (
            "Breakfast (7:30 AM): 3 whole eggs + 2 egg whites, whole grain sourdough toast, half avocado, black coffee.\n"
            "Morning Snack (10:30 AM): Low-fat Greek yogurt (150g) with blueberries and 1 scoop vanilla whey.\n"
            "Lunch (1:00 PM): 200g grilled chicken breast, 1.5 cups brown rice or quinoa, roasted vegetables.\n"
            "Pre-Workout (4:00 PM): Crisp apple with 15g almond butter.\n"
            "Dinner (7:30 PM): 200g grilled fish or chicken, sweet potato mash, steamed asparagus with lemon drizzle.\n"
            "Hydration: Minimum 3.5 Liters filtered water daily."
        )

    else:
        # Overweight / Obese
        workout_notes = (
            f"Lean Shred & Metabolic Recomposition Routine prescribed for BMI {bmi} (Height: {height_cm}cm, Weight: {weight_kg}kg). "
            f"High-density supersets combined with low-impact cardiovascular conditioning to protect joints while maximizing fat oxidation."
        )
        exercises_data = [
            {"name": "Incline Treadmill Hill Walk", "category": "cardio", "sets": 1, "reps": None, "weight_kg": None, "duration_minutes": 25},
            {"name": "Kettlebell Goblet Squats", "category": "strength", "sets": 4, "reps": 12, "weight_kg": Decimal("18.00"), "duration_minutes": None},
            {"name": "Dumbbell Flat Chest Press", "category": "strength", "sets": 4, "reps": 12, "weight_kg": Decimal("16.00"), "duration_minutes": None},
            {"name": "Seated Cable Rows", "category": "strength", "sets": 4, "reps": 12, "weight_kg": Decimal("40.00"), "duration_minutes": None},
            {"name": "Cable Face Pulls", "category": "strength", "sets": 4, "reps": 15, "weight_kg": Decimal("20.00"), "duration_minutes": None},
            {"name": "Core Abdominal Plank", "category": "balance", "sets": 4, "reps": None, "weight_kg": None, "duration_minutes": 1},
            {"name": "Elliptical Zone 2 Stamina", "category": "cardio", "sets": 1, "reps": None, "weight_kg": None, "duration_minutes": 20},
        ]
        meal_schedule = (
            "Breakfast (7:30 AM): Egg white omelette (5 whites + 1 yolk) with baby spinach, tomatoes, green tea.\n"
            "Mid-Morning (10:30 AM): Whey isolate protein shake (30g protein) with cold water or unsweetened almond milk.\n"
            "Lunch (1:00 PM): 200g grilled turkey or chicken breast, 1 cup cooked quinoa, large cucumber and bell pepper salad.\n"
            "Afternoon Snack (4:00 PM): Crisp celery sticks with 1 tbsp hummus or handful of raw walnuts.\n"
            "Dinner (7:00 PM): 220g baked white fish (tilapia/cod) or grilled tofu, steamed broccoli & asparagus.\n"
            "Hydration: 4.0 Liters cold water daily."
        )

    # Save Workout Plan & Exercises
    wp = WorkoutPlan.objects.create(
        member=member,
        trainer=trainer,
        start_date=today,
        end_date=in_3_months,
        notes=workout_notes
    )

    for ex in exercises_data:
        Exercise.objects.create(
            workout_plan=wp,
            name=ex["name"],
            category=ex["category"],
            sets=ex["sets"],
            reps=ex["reps"],
            weight_kg=ex["weight_kg"],
            duration_minutes=ex["duration_minutes"]
        )

    # Save Diet Plan
    dp = DietPlan.objects.create(
        member=member,
        trainer=trainer,
        start_date=today,
        end_date=in_3_months,
        daily_calories=metrics['target_calories'],
        protein_g=metrics['protein_g'],
        carbs_g=metrics['carbs_g'],
        fat_g=metrics['fat_g'],
        meal_schedule={"schedule": meal_schedule}
    )

    return wp, dp, metrics
