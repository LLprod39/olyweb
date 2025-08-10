# main/dashboard.py

from .models import News, UsefulMaterial, ClanMember
from django.contrib.auth.models import User

def dashboard_callback(request, context):
    """
    This callback function populates the admin dashboard context with statistics.
    """
    # Get statistics from the database
    news_count = News.objects.count()
    materials_count = UsefulMaterial.objects.count()
    members_count = ClanMember.objects.count()
    users_count = User.objects.count()
    recent_news = News.objects.order_by('-created_at')[:5]
    recent_materials = UsefulMaterial.objects.order_by('-created_at')[:5]

    # Update the context with the new data
    context.update({
        "news_count": news_count,
        "materials_count": materials_count,
        "members_count": members_count,
        "users_count": users_count,
        "recent_news": recent_news,
        "recent_materials": recent_materials,
        "site_title": "OlyWeb Admin",
    })

    return context
