# 📰 Руководство по автоматическому добавлению новостей

## Обзор

В данном руководстве описаны различные способы автоматического добавления новостей в Django проект через админ-панель и программные методы.

## Методы добавления новостей

### 1. Django Management Command (Рекомендуемый способ)

Создан файл `main/management/commands/add_news.py` для добавления новостей через командную строку.

#### Использование:

```bash
# Добавление новостей из JSON файла
python manage.py add_news --file sample_news.json

# Добавление одной новости через параметры
python manage.py add_news --title "Заголовок новости" --content "Содержание новости" --category clan --author admin

# Добавление неопубликованной новости
python manage.py add_news --title "Черновик" --content "Текст черновика" --published False
```

#### Параметры команды:
- `--file` - путь к JSON файлу с новостями
- `--title` - заголовок новости
- `--content` - содержание новости
- `--category` - категория (game, clan, events, updates)
- `--author` - имя пользователя автора
- `--published` - опубликовать новость (True/False)

### 2. Python скрипт

Создан файл `auto_news_script.py` для более гибкого управления новостями.

#### Использование:

```bash
# Добавление новостей из JSON файла
python auto_news_script.py --json sample_news.json

# Интерактивное создание новости
python auto_news_script.py --interactive

# Показать справку
python auto_news_script.py --help
```

### 3. Прямое использование Django ORM

```python
from django.contrib.auth.models import User
from main.models import News

# Получаем или создаем пользователя
author, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@example.com', 'is_staff': True}
)

# Создаем новость
news = News.objects.create(
    title='Заголовок новости',
    content='Содержание новости',
    category='clan',
    author=author,
    is_published=True
)
```

## Структура модели News

```python
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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='clan')
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```

## Формат JSON файла

```json
[
    {
        "title": "Заголовок новости",
        "content": "Содержание новости с поддержкой HTML",
        "category": "clan",
        "author": "admin",
        "is_published": true
    },
    {
        "title": "Еще одна новость",
        "content": "Другое содержание",
        "category": "events",
        "author": "clan_leader",
        "is_published": false
    }
]
```

## Пошаговая инструкция

### Шаг 1: Подготовка

1. Убедитесь, что Django проект запущен и база данных настроена
2. Активируйте виртуальное окружение (если используется)
3. Перейдите в корневую директорию проекта

### Шаг 2: Создание JSON файла с новостями

Создайте файл `my_news.json` с вашими новостями:

```json
[
    {
        "title": "Ваша первая новость",
        "content": "Содержание первой новости",
        "category": "clan",
        "author": "admin",
        "is_published": true
    }
]
```

### Шаг 3: Запуск команды

```bash
# Используя Django management command
python manage.py add_news --file my_news.json

# Или используя Python скрипт
python auto_news_script.py --json my_news.json
```

### Шаг 4: Проверка результата

1. Откройте админ-панель Django: `http://localhost:8000/admin/`
2. Перейдите в раздел "Новости"
3. Убедитесь, что новости добавлены

## Автоматизация через cron (Linux/Mac)

### Создание скрипта для cron:

```bash
#!/bin/bash
# /path/to/add_news_cron.sh

cd /path/to/your/django/project
source venv/bin/activate
python manage.py add_news --file /path/to/news.json
```

### Настройка cron:

```bash
# Открыть crontab для редактирования
crontab -e

# Добавить строку для запуска каждый день в 9:00
0 9 * * * /path/to/add_news_cron.sh
```

## Автоматизация через Task Scheduler (Windows)

1. Откройте "Планировщик задач"
2. Создайте новую задачу
3. Настройте триггер (например, ежедневно в 9:00)
4. Добавьте действие: запуск `python.exe` с параметрами скрипта

## Обработка ошибок

### Частые проблемы:

1. **Файл не найден**: Проверьте путь к JSON файлу
2. **Ошибка JSON**: Убедитесь в правильности формата JSON
3. **Дублирование новостей**: Скрипт автоматически проверяет существующие заголовки
4. **Ошибка автора**: Автоматически создается пользователь, если не существует

### Логирование:

Все операции логируются в консоль с цветными индикаторами:
- ✅ Успешно
- ❌ Ошибка
- ⚠️ Предупреждение

## Безопасность

1. **Валидация данных**: Все входные данные проверяются
2. **Создание пользователей**: Автоматически создаются только базовые пользователи
3. **Дублирование**: Предотвращается создание дублирующих новостей
4. **Права доступа**: Используются только существующие пользователи или создаются с минимальными правами

## Расширение функциональности

### Добавление изображений:

```python
# В JSON файле добавьте поле image_url
{
    "title": "Новость с изображением",
    "content": "Содержание",
    "image_url": "https://example.com/image.jpg",
    "category": "clan"
}
```

### Добавление тегов:

```python
# Расширьте модель News
tags = models.ManyToManyField('NewsTag', blank=True)
```

### Добавление планирования публикации:

```python
# Добавьте поле в модель
scheduled_at = models.DateTimeField(null=True, blank=True)
```

## Заключение

Данные инструменты позволяют эффективно автоматизировать процесс добавления новостей в Django проект. Выберите наиболее подходящий для ваших задач способ и следуйте инструкциям по настройке. 