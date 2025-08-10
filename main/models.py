from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class News(models.Model):
    CATEGORY_CHOICES = [
        ('game', 'Игра'),
        ('clan', 'Клан'),
        ('events', 'События'),
        ('updates', 'Обновления'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(verbose_name='Содержание')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='clan', verbose_name='Категория')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if not self.slug:
            return '#'
        return reverse('main:news_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

class UsefulMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('software', 'Софт'),
        ('builder', 'Билдер'),
        ('auction', 'Аукционный дом'),
        ('mods', 'Моды'),
        ('guides', 'Гайды'),
        ('patches', 'Патчи'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='software', verbose_name='Категория')
    download_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на загрузку')
    file = models.FileField(upload_to='useful_materials/', blank=True, null=True, verbose_name='Файл для загрузки')
    installation_guide = models.TextField(blank=True, null=True, verbose_name='Инструкция по установке')
    image = models.ImageField(upload_to='useful_materials/', blank=True, null=True, verbose_name='Изображение')
    version = models.CharField(max_length=50, blank=True, null=True, verbose_name='Версия')
    file_size = models.CharField(max_length=50, blank=True, null=True, verbose_name='Размер файла')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    downloads_count = models.PositiveIntegerField(default=0, verbose_name='Количество загрузок')
    
    class Meta:
        verbose_name = 'Полезный материал'
        verbose_name_plural = 'Полезные материалы'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        if not self.slug:
            return '#'
        return reverse('main:useful_material_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    def increment_downloads(self):
        """Увеличивает счетчик загрузок"""
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])

class ClanMember(models.Model):
    ROLE_CHOICES = [
        ('leader', 'Лидер'),
        ('officer', 'Офицер'),
        ('member', 'Участник'),
        ('recruit', 'Новичок'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='recruit', verbose_name='Роль')
    join_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата вступления')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    game_nickname = models.CharField(max_length=100, blank=True, verbose_name='Игровой никнейм')
    level = models.IntegerField(default=1, verbose_name='Уровень')
    experience = models.IntegerField(default=0, verbose_name='Опыт')
    last_seen = models.DateTimeField(auto_now=True, verbose_name='Последний раз онлайн')
    
    class Meta:
        verbose_name = 'Член клана'
        verbose_name_plural = 'Члены клана'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    @property
    def display_name(self):
        return self.game_nickname if self.game_nickname else self.user.username
    
    @property
    def is_online(self):
        """Проверяет, находится ли пользователь онлайн (активен в последние 5 минут)"""
        return self.last_seen >= timezone.now() - timedelta(minutes=5)
    
    def update_last_seen(self):
        """Обновляет время последней активности"""
        self.last_seen = timezone.now()
        self.save(update_fields=['last_seen']) 