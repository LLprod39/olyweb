#!/usr/bin/env python3
"""
Скрипт для автоматического добавления новостей в Django проект
Использование: python auto_news_script.py [опции]
"""

import os
import sys
import django
import json
from datetime import datetime

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_news.news_parser import parse_news

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olyweb.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import News


def create_news_from_json(json_file_path):
    """Создает новости из JSON файла"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            news_data = json.load(file)
        
        created_count = 0
        for news_item in news_data:
            if create_single_news(news_item):
                created_count += 1
        
        print(f"✅ Успешно создано {created_count} новостей из {len(news_data)}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Файл {json_file_path} не найден")
        return False
    except json.JSONDecodeError:
        print(f"❌ Ошибка при чтении JSON файла {json_file_path}")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False


def create_single_news(news_data):
    """Создает одну новость"""
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
        
        # Используем update_or_create для обновления или создания новости
        news, created = News.objects.update_or_create(
            title=news_data['title'],
            defaults={
                'content': news_data['content'],
                'category': news_data.get('category', 'clan'),
                'author': author,
                'is_published': news_data.get('is_published', True)
            }
        )
        
        if created:
            print(f"✅ Создана новость: '{news.title}' (ID: {news.id})")
        else:
            print(f"🔄 Обновлена новость: '{news.title}' (ID: {news.id})")
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании новости '{news_data.get('title', 'Unknown')}': {str(e)}")
        return False


def create_news_interactive():
    """Интерактивное создание новости"""
    print("\n📝 Создание новой новости:")
    print("-" * 40)
    
    title = input("Заголовок новости: ").strip()
    if not title:
        print("❌ Заголовок не может быть пустым")
        return False
    
    content = input("Содержание новости: ").strip()
    if not content:
        print("❌ Содержание не может быть пустым")
        return False
    
    print("\nДоступные категории:")
    print("1. game - Игра")
    print("2. clan - Клан")
    print("3. events - События")
    print("4. updates - Обновления")
    
    category_choice = input("Выберите категорию (1-4) или нажмите Enter для 'clan': ").strip()
    category_map = {'1': 'game', '2': 'clan', '3': 'events', '4': 'updates'}
    category = category_map.get(category_choice, 'clan')
    
    author = input("Имя автора (или Enter для 'admin'): ").strip() or 'admin'
    
    published = input("Опубликовать новость? (y/n, по умолчанию y): ").strip().lower()
    is_published = published != 'n'
    
    news_data = {
        'title': title,
        'content': content,
        'category': category,
        'author': author,
        'is_published': is_published
    }
    
    return create_single_news(news_data)


def run_parser_and_create_news():
    """Запускает парсер и создает новости в интерактивном режиме"""
    print("🚀 Запуск парсера для получения списка новостей...")
    parse_news()
    print("✅ Парсер завершил работу.")

    json_file = 'bot_news/parsed_news.json'
    if not os.path.exists(json_file):
        print(f"❌ Файл {json_file} не найден после парсинга.")
        return

    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            news_data = json.load(file)
    except Exception as e:
        print(f"❌ Ошибка при чтении файла {json_file}: {e}")
        return

    print("\n" + "="*50)
    print("ИНТЕРАКТИВНОЕ ДОБАВЛЕНИЕ НОВОСТЕЙ")
    print("="*50)
    print("Сайт использует динамическую загрузку контента, поэтому требуется ручной ввод.")
    
    created_count = 0
    for i, news_item in enumerate(news_data):
        print(f"\n--- Новость {i+1}/{len(news_data)} ---")
        print(f"Заголовок: {news_item['title']}")
        print(f"URL: {news_item['source_url']}")
        
        # Проверяем, существует ли новость с таким заголовком
        if News.objects.filter(title=news_item['title']).exists():
            update_choice = input("ℹ️  Новость с таким заголовком уже существует. Хотите обновить ее? (y/n): ").strip().lower()
            if update_choice != 'y':
                print("⏩ Обновление пропущено.")
                continue
        
        print("\nДействие:")
        print("1. Откройте URL в браузере.")
        print("2. Скопируйте HTML-код содержимого статьи.")
        print("   (В Chrome: выделите текст -> правый клик -> 'Просмотреть код' -> на выделенном блоке правый клик -> 'Copy' -> 'Copy outerHTML')")
        
        content = input("3. Вставьте HTML-код сюда и нажмите Enter (оставьте пустым для пропуска): \n").strip()

        if not content:
            print("⏩ Новость пропущена.")
            continue

        # Обновляем данные новости с ручным вводом
        news_item['content'] = content
        
        if create_single_news(news_item):
            created_count += 1

    print(f"\n✅ Успешно создано {created_count} новых новостей.")


def show_help():
    """Показывает справку по использованию"""
    print("""
📰 Скрипт для автоматического добавления новостей

Использование:
    python auto_news_script.py [опция]

Опции:
    --parse          - Спарсить новости и добавить их в базу данных
    --json <файл>     - Добавить новости из JSON файла
    --interactive     - Интерактивное создание новости
    --help           - Показать эту справку

Примеры:
    python auto_news_script.py --parse
    python auto_news_script.py --json sample_news.json
    python auto_news_script.py --interactive

Формат JSON файла:
    [
        {
            "title": "Заголовок новости",
            "content": "Содержание новости",
            "category": "clan",
            "author": "admin",
            "is_published": true
        }
    ]

Доступные категории: game, clan, events, updates
    """)


def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    option = sys.argv[1]
    
    if option == '--help':
        show_help()
    elif option == '--parse':
        run_parser_and_create_news()
    elif option == '--json':
        if len(sys.argv) < 3:
            print("❌ Укажите путь к JSON файлу")
            return
        json_file = sys.argv[2]
        create_news_from_json(json_file)
    elif option == '--interactive':
        create_news_interactive()
    else:
        print(f"❌ Неизвестная опция: {option}")
        show_help()


if __name__ == '__main__':
    main()
