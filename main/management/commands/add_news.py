from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import News
import json
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Автоматическое добавление новостей из JSON файла или через параметры'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Путь к JSON файлу с новостями'
        )
        parser.add_argument(
            '--title',
            type=str,
            help='Заголовок новости'
        )
        parser.add_argument(
            '--content',
            type=str,
            help='Содержание новости'
        )
        parser.add_argument(
            '--category',
            type=str,
            choices=['game', 'clan', 'events', 'updates'],
            default='clan',
            help='Категория новости'
        )
        parser.add_argument(
            '--author',
            type=str,
            default='admin',
            help='Имя пользователя автора'
        )
        parser.add_argument(
            '--published',
            type=bool,
            default=True,
            help='Опубликовать новость (True/False)'
        )

    def handle(self, *args, **options):
        if options['file']:
            self.add_news_from_file(options['file'])
        elif options['title'] and options['content']:
            self.add_single_news(options)
        else:
            self.stdout.write(
                self.style.ERROR('Необходимо указать --file или --title и --content')
            )

    def add_news_from_file(self, file_path):
        """Добавляет новости из JSON файла"""
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'Файл {file_path} не найден')
            )
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                news_data = json.load(file)

            if not isinstance(news_data, list):
                self.stdout.write(
                    self.style.ERROR('JSON файл должен содержать массив новостей')
                )
                return

            for news_item in news_data:
                self.create_news(news_item)

        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('Ошибка при чтении JSON файла')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка: {str(e)}')
            )

    def add_single_news(self, options):
        """Добавляет одну новость через параметры командной строки"""
        news_data = {
            'title': options['title'],
            'content': options['content'],
            'category': options['category'],
            'author': options['author'],
            'is_published': options['published']
        }
        self.create_news(news_data)

    def create_news(self, news_data):
        """Создает новость в базе данных"""
        try:
            # Получаем или создаем пользователя-автора
            author, created = User.objects.get_or_create(
                username=news_data.get('author', 'admin'),
                defaults={
                    'email': f"{news_data.get('author', 'admin')}@example.com",
                    'is_staff': True,
                    'is_superuser': True
                }
            )

            # Проверяем, существует ли уже новость с таким заголовком
            existing_news = News.objects.filter(title=news_data['title']).first()
            if existing_news:
                self.stdout.write(
                    self.style.WARNING(f'Новость "{news_data["title"]}" уже существует')
                )
                return

            # Создаем новость
            news = News.objects.create(
                title=news_data['title'],
                content=news_data['content'],
                category=news_data.get('category', 'clan'),
                author=author,
                is_published=news_data.get('is_published', True)
            )

            self.stdout.write(
                self.style.SUCCESS(f'Создана новость: "{news.title}" (ID: {news.id})')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании новости "{news_data.get("title", "Unknown")}": {str(e)}')
            ) 