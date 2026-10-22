from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import GymItem
from apps.membership.models import MembershipPlan
from apps.trainers.models import Trainer
from apps.members.models import Member
from apps.workouts.models import WorkoutPlan
from apps.diets.models import DietPlan

def home(request):
    plans = MembershipPlan.objects.filter(is_active=True)[:4]
    trainers = Trainer.objects.select_related('user')[:4]
    equipments = GymItem.objects.all()[:6]
    
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='active').count()
    total_trainers = Trainer.objects.count()
    total_equipments = GymItem.objects.count()
    
    context = {
        'plans': plans,
        'trainers': trainers,
        'equipments': equipments,
        'total_members': total_members,
        'active_members': active_members,
        'total_trainers': total_trainers,
        'total_equipments': total_equipments,
    }
    return render(request, 'core/home.html', context)

def general_dashboard(request):
    """Gym Catalog / Equipment Inventory View with Add Item Support"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', 'strength')
        quantity = request.POST.get('quantity', 1)
        status = request.POST.get('status', 'available')
        description = request.POST.get('description', '').strip()
        
        if name:
            try:
                qty_int = int(quantity) if quantity else 1
            except ValueError:
                qty_int = 1
                
            item = GymItem.objects.create(
                name=name,
                category=category,
                quantity=max(1, qty_int),
                status=status,
                description=description
            )
            messages.success(request, f"Equipment item '{item.name}' added to catalog successfully!")
            return redirect('core:general_dashboard')
        else:
            messages.error(request, "Please enter a valid item name.")
            
    items = GymItem.objects.all().order_by('-id')
    total_equipments = GymItem.objects.filter(status='available').count()
    maintenance_equipments = GymItem.objects.filter(status='maintenance').count()
    
    base_template = 'base.html' if request.user.is_authenticated else 'core/public_base.html'
    
    context = {
        'items': items,
        'total_equipments': total_equipments,
        'maintenance_equipments': maintenance_equipments,
        'base_template': base_template,
    }
    return render(request, 'core/general_dashboard.html', context)

def customer_reviews(request):
    """Customer Reviews & Member Feedback Showcase View"""
    # Initialize default reviews in session if not present
    if 'reviews_list' not in request.session:
        request.session['reviews_list'] = [
            {
                'author': 'Kumaran R P',
                'role': 'VIP Member',
                'rating': 5,
                'date': '2 days ago',
                'comment': 'Muscle n Fitness has completely changed my fitness journey. The personal trainers, modern equipment, and customized diet plans are world-class!'
            },
            {
                'author': 'Guy Hawkins',
                'role': 'Pro Athlete',
                'rating': 5,
                'date': '1 week ago',
                'comment': 'State-of-the-art free weights, Olympic barbells, and clean recovery facilities. The best gym management system in the region.'
            },
            {
                'author': 'Danny Liu',
                'role': 'Annual Subscriber',
                'rating': 5,
                'date': '2 weeks ago',
                'comment': 'The attendance tracking and mobile routine viewer make every workout seamless. Highly recommend to anyone serious about health.'
            },
            {
                'author': 'Bella Deviant',
                'role': 'Cardio & Strength Enthusiast',
                'rating': 5,
                'date': '3 weeks ago',
                'comment': 'Friendly trainers, pristine equipment, and an energetic atmosphere. 5 stars all the way!'
            }
        ]

    if request.method == 'POST':
        author = request.POST.get('author', '').strip() or (request.user.get_full_name() if request.user.is_authenticated else 'Member')
        role = request.POST.get('role', 'Gym Member').strip() or 'Gym Member'
        rating = request.POST.get('rating', '5')
        comment = request.POST.get('comment', '').strip()
        
        if comment:
            try:
                rating_int = int(rating)
            except ValueError:
                rating_int = 5
                
            new_review = {
                'author': author,
                'role': role,
                'rating': rating_int,
                'date': 'Just now',
                'comment': comment
            }
            reviews = request.session.get('reviews_list', [])
            reviews.insert(0, new_review)
            request.session['reviews_list'] = reviews
            messages.success(request, "Thank you! Your review has been published successfully.")
            return redirect('core:customer_reviews')
        else:
            messages.error(request, "Please enter your review feedback comment.")

    reviews = request.session.get('reviews_list', [])
    base_template = 'base.html' if request.user.is_authenticated else 'core/public_base.html'
    
    return render(request, 'core/reviews.html', {
        'reviews': reviews,
        'base_template': base_template
    })
