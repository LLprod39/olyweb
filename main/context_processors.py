from django.db.models import Count
from .models import News, UsefulMaterial, ClanMember
from django.contrib.auth.models import User

def admin_stats(request):
    """Добавляет статистику для админки"""
    if request.path.startswith('/admin/'):
        return {
            'news_count': News.objects.count(),
            'materials_count': UsefulMaterial.objects.count(),
            'members_count': ClanMember.objects.count(),
            'users_count': User.objects.count(),
            'recent_news': News.objects.order_by('-created_at')[:5],
            'recent_materials': UsefulMaterial.objects.order_by('-created_at')[:5],
        }
    return {}
