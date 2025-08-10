from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from datetime import timedelta
from .models import News, ClanMember, UsefulMaterial

def home(request):
    """Главная страница сайта"""
    try:
        # Получаем последние новости
        latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:6]
        
        # Статистика клана
        approved_members = ClanMember.objects.filter(is_active=True, is_approved=True)
        online_members = [member for member in approved_members if member.is_online]
        
        # Обновляем время последней активности для авторизованного пользователя
        if request.user.is_authenticated:
            try:
                clan_member = ClanMember.objects.get(user=request.user)
                clan_member.update_last_seen()
            except ClanMember.DoesNotExist:
                pass
        
        clan_stats = {
            'total_members': approved_members.count(),
            'online_members': len(online_members),
            'clan_level': 5,  # Заглушка, в будущем можно получать из API игры
        }
        
        context = {
            'latest_news': latest_news,
            'clan_stats': clan_stats,
        }
        return render(request, 'main/home.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке главной страницы.')
        context = {
            'latest_news': [],
            'clan_stats': {'total_members': 0, 'online_members': 0, 'clan_level': 1},
        }
        return render(request, 'main/home.html', context)

def about(request):
    """Страница о клане"""
    try:
        # Получаем статистику клана
        approved_members = ClanMember.objects.filter(is_active=True, is_approved=True)
        online_members = [member for member in approved_members if member.is_online]
        
        clan_stats = {
            'total_members': approved_members.count(),
            'online_members': len(online_members),
            'clan_level': 5,
        }
        
        context = {
            'clan_stats': clan_stats,
        }
        return render(request, 'main/about.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке страницы о клане.')
        context = {
            'clan_stats': {'total_members': 0, 'online_members': 0, 'clan_level': 1},
        }
        return render(request, 'main/about.html', context)

def members(request):
    """Страница участников клана с фильтрацией"""
    try:
        # Получаем параметры фильтрации
        role = request.GET.get('role', '')
        status = request.GET.get('status', '')
        search = request.GET.get('search', '')
        
        # Базовый queryset
        members_queryset = ClanMember.objects.filter(is_active=True, is_approved=True)
        
        # Применяем фильтры
        if role:
            members_queryset = members_queryset.filter(role=role)
        
        if status == 'online':
            members_queryset = [member for member in members_queryset if member.is_online]
        elif status == 'offline':
            members_queryset = [member for member in members_queryset if not member.is_online]
        
        if search:
            # Поиск по игровому нику или имени пользователя
            filtered_members = []
            for member in members_queryset:
                if (search.lower() in member.game_nickname.lower() or 
                    search.lower() in member.user.username.lower()):
                    filtered_members.append(member)
            members_queryset = filtered_members
        
        # Сортировка по роли и уровню
        if isinstance(members_queryset, list):
            members_queryset = sorted(members_queryset, 
                                    key=lambda x: (x.role != 'leader', x.role != 'officer', -x.level))
        else:
            members_queryset = members_queryset.order_by('role', '-level')
        
        # Статистика клана
        approved_members = ClanMember.objects.filter(is_active=True, is_approved=True)
        online_members = [member for member in approved_members if member.is_online]
        
        clan_stats = {
            'total_members': approved_members.count(),
            'online_members': len(online_members),
            'clan_level': 5,
        }
        
        context = {
            'members': members_queryset,
            'clan_stats': clan_stats,
        }
        return render(request, 'main/members.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке участников клана.')
        context = {
            'members': [],
            'clan_stats': {'total_members': 0, 'online_members': 0, 'clan_level': 1},
        }
        return render(request, 'main/members.html', context)

def news_list(request):
    """Список всех новостей с поиском и фильтрацией"""
    try:
        # Получаем параметры фильтрации и поиска
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        
        # Базовый queryset
        news_queryset = News.objects.filter(is_published=True)
        
        # Применяем фильтры
        if category:
            news_queryset = news_queryset.filter(category=category)
        
        if search:
            # Поиск по заголовку, содержанию и автору
            news_queryset = news_queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(author__username__icontains=search)
            )
        
        # Сортировка
        news_queryset = news_queryset.order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(news_queryset, 9)  # 9 новостей на страницу
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Получаем категории для фильтра
        categories = News.CATEGORY_CHOICES
        
        # Статистика по категориям
        category_stats = {}
        for cat_code, cat_name in categories:
            category_stats[cat_code] = News.objects.filter(
                category=cat_code, 
                is_published=True
            ).count()
        
        context = {
            'news_list': page_obj,
            'page_obj': page_obj,
            'categories': categories,
            'current_category': category,
            'search_query': search,
            'category_stats': category_stats,
        }
        return render(request, 'main/news_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке новостей.')
        return render(request, 'main/news_list.html', {'news_list': [], 'page_obj': None})

def news_detail(request, slug):
    """Детальная страница новости с похожими новостями"""
    try:
        news = get_object_or_404(News, slug=slug, is_published=True)
        
        # Получаем похожие новости (той же категории)
        related_news = News.objects.filter(
            category=news.category,
            is_published=True
        ).exclude(id=news.id).order_by('-created_at')[:4]
        
        # Если похожих новостей мало, добавляем новости других категорий
        if related_news.count() < 4:
            additional_news = News.objects.filter(
                is_published=True
            ).exclude(
                id__in=[news.id] + list(related_news.values_list('id', flat=True))
            ).order_by('-created_at')[:4 - related_news.count()]
            related_news = list(related_news) + list(additional_news)
        
        # Получаем статистику просмотров (можно добавить поле views в модель)
        # news.views += 1
        # news.save()
        
        context = {
            'news': news,
            'related_news_list': related_news,
        }
        return render(request, 'main/news_detail.html', context)
    except News.DoesNotExist:
        messages.error(request, 'Новость не найдена.')
        return redirect('main:news_list')
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке новости.')
        return redirect('main:news_list')

@login_required
def join_clan(request):
    """Заявка на вступление в клан"""
    try:
        # Проверяем, не является ли пользователь уже членом клана
        existing_member = ClanMember.objects.filter(user=request.user).first()
        
        if existing_member:
            if existing_member.is_approved:
                messages.info(request, 'Вы уже являетесь членом клана.')
                return redirect('main:home')
            else:
                messages.info(request, 'Ваша заявка уже находится на рассмотрении.')
                return redirect('main:home')
        
        if request.method == 'POST':
            game_nickname = request.POST.get('game_nickname', '').strip()
            level = request.POST.get('level', 1)
            experience = request.POST.get('experience', '')
            
            if not game_nickname:
                messages.error(request, 'Пожалуйста, укажите игровой никнейм.')
                return render(request, 'main/join_clan.html')
            
            try:
                level = int(level)
                if level < 1:
                    level = 1
            except ValueError:
                level = 1
            
            try:
                experience = int(experience) if experience else 0
            except ValueError:
                experience = 0
            
            # Создаем заявку
            ClanMember.objects.create(
                user=request.user,
                role='recruit',
                game_nickname=game_nickname,
                level=level,
                experience=experience,
                is_approved=False
            )
            
            messages.success(request, 'Ваша заявка на вступление в клан отправлена! Ожидайте одобрения от администрации.')
            return redirect('main:home')
        
        return render(request, 'main/join_clan.html')
    except Exception as e:
        messages.error(request, 'Произошла ошибка при отправке заявки.')
        return redirect('main:home')

def news_by_category(request, category):
    """Новости по категории"""
    try:
        # Проверяем, что категория существует
        valid_categories = dict(News.CATEGORY_CHOICES)
        if category not in valid_categories:
            messages.error(request, 'Категория не найдена.')
            return redirect('main:news_list')
        
        # Получаем новости категории
        news_queryset = News.objects.filter(
            category=category,
            is_published=True
        ).order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(news_queryset, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'news_list': page_obj,
            'page_obj': page_obj,
            'current_category': category,
            'category_name': valid_categories[category],
        }
        return render(request, 'main/news_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке новостей категории.')
        return redirect('main:news_list')

def search_news(request):
    """Поиск новостей"""
    try:
        search_query = request.GET.get('q', '').strip()
        
        if not search_query:
            return redirect('main:news_list')
        
        # Поиск по заголовку, содержанию и автору
        news_queryset = News.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        ).order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(news_queryset, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'news_list': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
            'results_count': news_queryset.count(),
        }
        return render(request, 'main/news_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при поиске новостей.')
        return redirect('main:news_list') 

def useful_materials_list(request):
    """Список всех полезных материалов с поиском и фильтрацией"""
    try:
        # Получаем параметры фильтрации и поиска
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        
        # Базовый queryset
        materials_queryset = UsefulMaterial.objects.filter(is_published=True)
        
        # Применяем фильтры
        if category:
            materials_queryset = materials_queryset.filter(category=category)
        
        if search:
            # Поиск по названию, описанию и автору
            materials_queryset = materials_queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(author__username__icontains=search)
            )
        
        # Сортировка
        materials_queryset = materials_queryset.order_by('-created_at')
        
        # Получаем категории для фильтра
        categories = UsefulMaterial.CATEGORY_CHOICES
        
        # Статистика по категориям
        category_stats = {}
        for cat_code, cat_name in categories:
            category_stats[cat_code] = UsefulMaterial.objects.filter(
                category=cat_code, 
                is_published=True
            ).count()
        
        context = {
            'materials_list': materials_queryset,
            'categories': categories,
            'current_category': category,
            'search_query': search,
            'category_stats': category_stats,
        }
        return render(request, 'main/useful_materials_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке полезных материалов.')
        return render(request, 'main/useful_materials_list.html', {'materials_list': []})

def useful_material_detail(request, slug):
    """Детальная страница полезного материала"""
    try:
        material = get_object_or_404(UsefulMaterial, slug=slug, is_published=True)
        
        # Получаем похожие материалы (той же категории)
        related_materials = UsefulMaterial.objects.filter(
            category=material.category,
            is_published=True
        ).exclude(id=material.id).order_by('-created_at')[:4]
        
        # Если похожих материалов мало, добавляем материалы других категорий
        if related_materials.count() < 4:
            additional_materials = UsefulMaterial.objects.filter(
                is_published=True
            ).exclude(
                id__in=[material.id] + list(related_materials.values_list('id', flat=True))
            ).order_by('-created_at')[:4 - related_materials.count()]
            related_materials = list(related_materials) + list(additional_materials)
        
        context = {
            'material': material,
            'related_materials_list': related_materials,
        }
        return render(request, 'main/useful_material_detail.html', context)
    except UsefulMaterial.DoesNotExist:
        messages.error(request, 'Материал не найден.')
        return redirect('main:useful_materials_list')
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке материала.')
        return redirect('main:useful_materials_list')

def download_material(request, slug):
    """Загрузка файла полезного материала"""
    try:
        material = get_object_or_404(UsefulMaterial, slug=slug, is_published=True)
        
        # Проверяем, есть ли файл для загрузки
        if not material.file:
            messages.error(request, 'Файл для загрузки не найден.')
            return redirect('main:useful_material_detail', slug=slug)
        
        # Проверяем, существует ли файл на диске
        file_path = material.file.path
        if not os.path.exists(file_path):
            messages.error(request, 'Файл не найден на сервере.')
            return redirect('main:useful_material_detail', slug=slug)
        
        # Увеличиваем счетчик загрузок
        material.increment_downloads()
        
        # Отправляем файл
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
            
    except UsefulMaterial.DoesNotExist:
        messages.error(request, 'Материал не найден.')
        return redirect('main:useful_materials_list')
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке файла.')
        return redirect('main:useful_materials_list')

def useful_materials_by_category(request, category):
    """Полезные материалы по категории"""
    try:
        # Проверяем, что категория существует
        valid_categories = dict(UsefulMaterial.CATEGORY_CHOICES)
        if category not in valid_categories:
            messages.error(request, 'Категория не найдена.')
            return redirect('main:useful_materials_list')
        
        # Получаем материалы категории
        materials_queryset = UsefulMaterial.objects.filter(
            category=category,
            is_published=True
        ).order_by('-created_at')
        
        context = {
            'materials_list': materials_queryset,
            'current_category': category,
            'category_name': valid_categories[category],
        }
        return render(request, 'main/useful_materials_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при загрузке материалов категории.')
        return redirect('main:useful_materials_list')

def search_useful_materials(request):
    """Поиск полезных материалов"""
    try:
        search_query = request.GET.get('q', '').strip()
        
        if not search_query:
            return redirect('main:useful_materials_list')
        
        # Поиск по названию, описанию и автору
        materials_queryset = UsefulMaterial.objects.filter(
            is_published=True
        ).filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(author__username__icontains=search_query)
        ).order_by('-created_at')
        
        context = {
            'materials_list': materials_queryset,
            'search_query': search_query,
            'results_count': materials_queryset.count(),
        }
        return render(request, 'main/useful_materials_list.html', context)
    except Exception as e:
        messages.error(request, 'Произошла ошибка при поиске материалов.')
        return redirect('main:useful_materials_list') 