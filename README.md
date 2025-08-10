# OlyWeb — сайт клана Throne and Liberty (Eternal)

### Описание
OlyWeb — это веб‑сайт клана для игры Throne and Liberty. Проект объединяет новостной раздел, список участников клана, страницу полезных материалов и систему аутентификации. Подходит для презентации клана, координации игроков и публикации контента.

- **Демо-цель**: показать основу сайта клана и готовые модули
- **Стек**: Django 4.1, HTML/CSS/JS, SQLite (dev), Pillow, Selenium (для парсинга новостей)

---

### Возможности
- Новости клана/игры с категориями и поиском
- Список участников клана с фильтрами (роль/онлайн/поиск)
- Полезные материалы (файлы, ссылки, инструкции, счетчик загрузок)
- Регистрация, вход/выход, профиль пользователя с аватаром
- Заявка на вступление в клан (для авторизованных)
- Управляющие команды Django для демо-данных и новостей
- Скрипты для парсинга/автодобавления новостей (опционально)

---

### Требования
- Python 3.8+
- pip
- Git (желательно)
- Для парсинга новостей: Google Chrome и ChromeDriver (устанавливается автоматически через `webdriver-manager`)

---

### Быстрый старт (Windows/macOS/Linux)
1) Клонируйте репозиторий и перейдите в папку проекта:
```bash
git clone <repo-url>
cd olyweb
```
2) Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```
3) Установите зависимости:
```bash
pip install -r requirements.txt
```
4) Примените миграции и (по желанию) создайте суперпользователя:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # опционально
```
5) (Опционально) создайте демо-данные:
```bash
python manage.py create_sample_data
```
6) Запустите сервер разработки:
```bash
python manage.py runserver
```
Откройте `http://127.0.0.1:8000/`.

Админ-панель: `http://127.0.0.1:8000/admin/`.

---

### Маршруты (основные)
- `/` — главная страница
- `/about/` — о клане
- `/members/` — участники клана (фильтры: `?role=...&status=online|offline&search=...`)
- `/news/` — список новостей (фильтры: `?category=game|clan|events|updates&search=...`)
- `/news/<slug>/` — детальная новость
- `/useful/` — полезные материалы (фильтры: `?category=...&search=...`)
- `/useful/<slug>/` — детальный материал
- `/useful/<slug>/download/` — скачать файл материала
- `/join-clan/` — заявка на вступление (только авторизованные)
- `/auth/register/`, `/auth/login/`, `/auth/logout/`, `/auth/profile/`
- `/admin/` — админка Django

Файл маршрутов: `olyweb/urls.py`, приложения: `main/urls.py`, `auth_app/urls.py`.

---

### Структура проекта
```
olyweb/
├── auth_app/                 # Аутентификация и профиль
├── main/                     # Основной функционал сайта клана
│   ├── management/commands/  # Управляющие команды (демо-данные, новости, фикс slug)
│   ├── models.py             # News, UsefulMaterial, ClanMember
│   ├── urls.py, views.py     # Маршруты и представления
├── bot_news/                 # Скрипты парсинга/автодобавления новостей
├── bot/                      # Пример Discord-бота (см. безопасность ниже)
├── templates/                # HTML-шаблоны (base, main, auth_app)
├── static/                   # Статика (в т. ч. `css/mobile.css`, `js/mobile.js`)
├── media/                    # Медиа (аватары, новости, материалы)
├── olyweb/                   # Настройки и корневые URLs Django
├── manage.py                 # Точка входа Django
└── requirements.txt          # Зависимости
```

Приложение `accounts/` присутствует, но по умолчанию не подключено в `INSTALLED_APPS`.

---

### Модели данных (упрощенно)
- `main.models.News`:
  - `title`, `slug`, `content`, `category` (game|clan|events|updates), `image`, `author`, `is_published`, `created_at`, `updated_at`
- `main.models.UsefulMaterial`:
  - `title`, `slug`, `description`, `category`, `download_link`, `file`, `installation_guide`, `image`, `version`, `file_size`, `author`, `downloads_count`, `is_published`, timestamps
- `main.models.ClanMember`:
  - `user`, `role` (leader|officer|member|recruit), `game_nickname`, `level`, `experience`, `is_approved`, `is_active`, `last_seen`
  - Вспомогательные свойства: `display_name`, `is_online()`
- `auth_app.models.Profile`:
  - `user`, `bio`, `birth_date`, `avatar` (создается автоматически при создании пользователя)

---

### Шаблоны и статика
- Базовый шаблон: `templates/base.html`
- Разделы `templates/main/`: `home.html`, `about.html`, `members.html`, `news_list.html`, `news_detail.html`, `join_clan.html`, `useful_materials_list.html`, `useful_material_detail.html`
- Аутентификация `templates/auth_app/`: `home.html`, `register.html`, `login.html`, `profile.html`
- Статика настраивается через `STATICFILES_DIRS = [BASE_DIR / 'static']`
- Медиа: `MEDIA_ROOT = BASE_DIR / 'media'`, URL: `/media/`

---

### Управляющие команды
- Создать демо-данные (новости + участники):
```bash
python manage.py create_sample_data
```
- Добавить новости из JSON или параметров CLI:
```bash
# Из JSON
python manage.py add_news --file sample_news.json
# Один объект
python manage.py add_news --title "Заголовок" --content "Текст" --category clan --author admin --published True
```
- Исправить пустые slug у новостей:
```bash
python manage.py fix_empty_slugs
```

---

### Автоматизация/парсинг новостей (опционально)
Требования: Google Chrome установлен, доступ в интернет.

Вариант A. Скрипт с CLI-помощником `bot_news/auto_news_script.py`:
```bash
# Показать помощь
python bot_news/auto_news_script.py --help
# Добавить новости из JSON
python bot_news/auto_news_script.py --json bot_news/sample_news.json
# Интерактивно создать новость
python bot_news/auto_news_script.py --interactive
# Спарсить сайт и затем интерактивно добавить статьи
python bot_news/auto_news_script.py --parse
```
Внутри используется Django ORM (автоматически создаст автора при необходимости).

Вариант B. Парсер сайта `bot_news/news_parser.py` (Selenium):
```bash
python bot_news/news_parser.py
```
Результат сохраняется в `bot_news/parsed_news.json`. Далее импортируйте через вариант A или management-команду.

Подробное руководство: `bot_news/NEWS_AUTOMATION_GUIDE.md`.

---

### Конфигурация
- Файл настроек: `olyweb/settings.py`
- База данных (dev): SQLite `db.sqlite3`
- Аутентификация: редиректы `LOGIN_URL = '/auth/login/'`, `LOGIN_REDIRECT_URL = '/'`
- Домены: обновите `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` под ваш домен/туннель ngrok
  - Пример:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```

Примечание: переменные окружения по умолчанию не используются. Если хотите — добавьте загрузку из `.env` самостоятельно (например, через `python-dotenv`).

---

### Безопасность
- Никогда не храните секреты в репозитории. В проекте есть пример `bot/bot.py` с токеном Discord — его нужно немедленно заменить на чтение из переменных окружения и удалить из истории репозитория.
- Замените `SECRET_KEY` и не храните его в открытом доступе.
- В продакшене отключайте `DEBUG` и используйте надежную БД (PostgreSQL/MySQL), настроенный веб-сервер и HTTPS.

---

### Развертывание (кратко)
- Настройте PostgreSQL/MySQL
- Пропишите `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS`
- Соберите статику: 
```bash
python manage.py collectstatic
```
- Запустите приложение через WSGI/ASGI (например, Gunicorn/Uvicorn) за обратным прокси (Nginx)
- Настройте хранение медиа (S3/диск)

---

### Траблшутинг
- Ошибки миграций: удалите `db.sqlite3` (dev), пересоберите миграции и примените их
- Проблемы с Selenium: убедитесь, что установлен Chrome; обновите `webdriver-manager`
- Ошибки CSRF при доступе по домену: добавьте домен в `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS`
- Загрузка файлов: проверьте права на папку `media/`

---

### Полезные ссылки и файлы
- Технический план: `DEVELOPMENT_PLAN.md`
- Описание проекта: `PROJECT_DESCRIPTION.md`
- Гайд по новостям: `bot_news/NEWS_AUTOMATION_GUIDE.md`

---

### Лицензия
Лицензия не указана. Добавьте файл `LICENSE` при необходимости.

---

Сделано для сообщества клана Eternal в Throne and Liberty. 🚀
