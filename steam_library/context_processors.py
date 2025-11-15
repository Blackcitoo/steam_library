"""
Context processors personalizados
"""
from library.models import Notification


def notifications_count(request):
    """Agrega el conteo de notificaciones no leídas al contexto"""
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}

