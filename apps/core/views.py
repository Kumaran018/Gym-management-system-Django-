from django.shortcuts import render
from .models import GymItem

def home(request):
    return render(request, 'core/home.html')

def general_dashboard(request):
    items = GymItem.objects.all()
    # Simple stats for overview counters
    total_equipments = GymItem.objects.filter(status='available').count()
    maintenance_equipments = GymItem.objects.filter(status='maintenance').count()
    
    # Choose base shell layout dynamically
    base_template = 'base.html' if request.user.is_authenticated else 'core/public_base.html'
    
    context = {
        'items': items,
        'total_equipments': total_equipments,
        'maintenance_equipments': maintenance_equipments,
        'base_template': base_template,
    }
    return render(request, 'core/general_dashboard.html', context)

