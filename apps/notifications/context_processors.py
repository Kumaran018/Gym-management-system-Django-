from .models import Notification

def notifications_context(request):
    if request.user.is_authenticated:
        user_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
        unread_count = user_notifs.filter(is_read=False).count()
        total_count = user_notifs.count()
        return {
            'nav_notifications': user_notifs[:8],
            'nav_unread_count': unread_count,
            'nav_total_notifications': total_count,
        }
    return {
        'nav_notifications': [],
        'nav_unread_count': 0,
        'nav_total_notifications': 0,
    }
