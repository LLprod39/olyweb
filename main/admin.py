from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from datetime import timedelta
from .models import News, ClanMember, UsefulMaterial

class PublishedFilter(SimpleListFilter):
    title = 'Статус публикации'
    parameter_name = 'published_status'

    def lookups(self, request, model_admin):
        return (
            ('published', 'Опубликовано'),
            ('unpublished', 'Не опубликовано'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'published':
            return queryset.filter(is_published=True)
        if self.value() == 'unpublished':
            return queryset.filter(is_published=False)

class OnlineFilter(SimpleListFilter):
    title = 'Статус онлайн'
    parameter_name = 'online_status'

    def lookups(self, request, model_admin):
        return (
            ('online', 'Онлайн'),
            ('offline', 'Оффлайн'),
        )

    def queryset(self, request, queryset):
        five_minutes_ago = timezone.now() - timedelta(minutes=5)
        if self.value() == 'online':
            return queryset.filter(last_seen__gte=five_minutes_ago)
        if self.value() == 'offline':
            return queryset.filter(last_seen__lt=five_minutes_ago)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'is_published', 'get_image_preview')
    list_filter = (PublishedFilter, 'category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 20
    list_editable = ('is_published',)
    actions = ['make_published', 'make_unpublished']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'category', 'author')
        }),
        ('Медиа', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Нет изображения"
    get_image_preview.short_description = 'Изображение'
    
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} новостей было опубликовано.')
    make_published.short_description = "Опубликовать выбранные новости"
    
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} новостей было снято с публикации.')
    make_unpublished.short_description = "Снять с публикации выбранные новости"

@admin.register(UsefulMaterial)
class UsefulMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'version', 'downloads_count', 'author', 'created_at', 'is_published', 'get_file_preview')
    list_filter = (PublishedFilter, 'category', 'created_at', 'author')
    search_fields = ('title', 'description', 'installation_guide', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 20
    list_editable = ('is_published',)
    actions = ['make_published', 'make_unpublished', 'reset_downloads']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'category', 'version', 'file_size', 'author')
        }),
        ('Файлы и ссылки', {
            'fields': ('download_link', 'file', 'image'),
            'classes': ('collapse',)
        }),
        ('Инструкция по установке', {
            'fields': ('installation_guide',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('downloads_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
    )
    
    readonly_fields = ('downloads_count', 'created_at', 'updated_at')
    
    def get_file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📁 Файл</a>', obj.file.url)
        elif obj.download_link:
            return format_html('<a href="{}" target="_blank">🔗 Ссылка</a>', obj.download_link)
        return "Нет файла"
    get_file_preview.short_description = 'Файл/Ссылка'
    
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} материалов было опубликовано.')
    make_published.short_description = "Опубликовать выбранные материалы"
    
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} материалов было снято с публикации.')
    make_unpublished.short_description = "Снять с публикации выбранные материалы"
    
    def reset_downloads(self, request, queryset):
        updated = queryset.update(downloads_count=0)
        self.message_user(request, f'Счетчик загрузок сброшен для {updated} материалов.')
    reset_downloads.short_description = "Сбросить счетчик загрузок"

@admin.register(ClanMember)
class ClanMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'game_nickname', 'level', 'join_date', 'is_active', 'is_approved', 'get_online_status')
    list_filter = (OnlineFilter, 'role', 'is_active', 'is_approved', 'join_date', 'level')
    search_fields = ('user__username', 'user__email', 'game_nickname')
    list_per_page = 20
    list_editable = ('is_active', 'is_approved', 'role')
    actions = ['approve_members', 'disapprove_members', 'activate_members', 'deactivate_members']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'role', 'game_nickname', 'level', 'experience')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_approved')
        }),
        ('Даты', {
            'fields': ('join_date', 'last_seen'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('join_date', 'last_seen')
    
    def get_online_status(self, obj):
        if obj.is_online:
            return format_html('<span style="color: green;">🟢 Онлайн</span>')
        else:
            return format_html('<span style="color: red;">🔴 Оффлайн</span>')
    get_online_status.short_description = 'Статус'
    
    def approve_members(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} членов клана было одобрено.')
    approve_members.short_description = "Одобрить выбранных членов"
    
    def disapprove_members(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} членов клана было отклонено.')
    disapprove_members.short_description = "Отклонить выбранных членов"
    
    def activate_members(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} членов клана было активировано.')
    activate_members.short_description = "Активировать выбранных членов"
    
    def deactivate_members(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} членов клана было деактивировано.')
    deactivate_members.short_description = "Деактивировать выбранных членов" 