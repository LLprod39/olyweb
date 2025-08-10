from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import News, ClanMember
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Создает тестовые данные для сайта клана'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')
        
        # Создаем тестового пользователя если его нет
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eternal-clan.com',
                'first_name': 'Администратор',
                'last_name': 'Клана',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Создан пользователь admin с паролем admin123')
        
        # Создаем тестовые новости
        news_data = [
            {
                'title': 'Обновление Throne and Liberty - Новые возможности PvP',
                'content': '''
                Дорогие игроки! Команда разработчиков Throne and Liberty выпустила крупное обновление, которое добавляет множество новых возможностей для PvP сражений.

                <h3>Основные изменения:</h3>
                <ul>
                    <li>Новые арены для PvP сражений</li>
                    <li>Система рейтингов и рангов</li>
                    <li>Улучшенная система наград</li>
                    <li>Новые способности для всех классов</li>
                </ul>

                <p>Наш клан уже готов к новым вызовам! Присоединяйтесь к нам и станьте частью сильнейшего сообщества в игре.</p>

                <blockquote>
                    "Это обновление кардинально изменит PvP сцены в игре. Мы готовы показать, что Eternal - лучший клан!" - Лидер клана
                </blockquote>
                ''',
                'category': 'game'
            },
            {
                'title': 'Победа в турнире кланов - Eternal на вершине!',
                'content': '''
                Поздравляем всех участников клана Eternal с блестящей победой в еженедельном турнире кланов!

                <h3>Результаты турнира:</h3>
                <ul>
                    <li>1 место - Eternal Clan</li>
                    <li>2 место - Dark Legion</li>
                    <li>3 место - Storm Riders</li>
                </ul>

                <p>Наши игроки показали отличную командную работу и стратегическое мышление. Особую благодарность выражаем:</p>
                <ul>
                    <li>@WarriorMaster - за отличную координацию</li>
                    <li>@MagePro - за невероятные комбо</li>
                    <li>@HealerQueen - за безупречную поддержку</li>
                </ul>

                <p>Следующий турнир состоится через неделю. Готовьтесь к новым победам!</p>
                ''',
                'category': 'clan'
            },
            {
                'title': 'Анонс: Рейд на Древнего Дракона',
                'content': '''
                Внимание, участники клана! В эту субботу мы проводим масштабный рейд на Древнего Дракона!

                <h3>Детали события:</h3>
                <ul>
                    <li><strong>Дата:</strong> Суббота, 20:00 МСК</li>
                    <li><strong>Уровень:</strong> 50+</li>
                    <li><strong>Награды:</strong> Эпические предметы, опыт, золото</li>
                    <li><strong>Количество участников:</strong> 25 человек</li>
                </ul>

                <h3>Требования к участникам:</h3>
                <ul>
                    <li>Минимальный уровень 50</li>
                    <li>Наличие Discord для голосовой связи</li>
                    <li>Готовность к длительному рейду (2-3 часа)</li>
                    <li>Базовые знания механик босса</li>
                </ul>

                <p>Записывайтесь в Discord канале #рейды. Удачи всем участникам!</p>
                ''',
                'category': 'events'
            },
            {
                'title': 'Исправления багов в последнем патче',
                'content': '''
                Разработчики Throne and Liberty выпустили горячий патч с исправлениями критических багов.

                <h3>Исправленные проблемы:</h3>
                <ul>
                    <li>Исправлен баг с застреванием персонажей в текстурах</li>
                    <li>Устранена проблема с отображением урона в PvP</li>
                    <li>Исправлен баг с дублированием предметов</li>
                    <li>Улучшена стабильность серверов</li>
                </ul>

                <h3>Известные проблемы:</h3>
                <ul>
                    <li>Временные лаги в переполненных зонах</li>
                    <li>Проблемы с отображением некоторых эффектов</li>
                </ul>

                <p>Размер патча: 2.3 GB</p>
                <p>Время установки: ~15 минут</p>

                <p>Рекомендуем всем участникам клана обновить игру перед следующими рейдами.</p>
                ''',
                'category': 'updates'
            },
            {
                'title': 'Новые участники клана - Добро пожаловать!',
                'content': '''
                Клан Eternal продолжает расти! Мы рады приветствовать новых участников, присоединившихся к нашему сообществу.

                <h3>Новые участники:</h3>
                <ul>
                    <li>@ShadowHunter - Охотник, уровень 45</li>
                    <li>@LightMage - Маг, уровень 42</li>
                    <li>@IronTank - Танк, уровень 48</li>
                    <li>@SwiftRogue - Разбойник, уровень 40</li>
                </ul>

                <p>Все новички прошли испытательный срок и показали отличные результаты в командной работе.</p>

                <h3>Напоминание для новичков:</h3>
                <ul>
                    <li>Изучите правила клана в Discord</li>
                    <li>Присоединитесь к голосовым каналам</li>
                    <li>Участвуйте в ежедневных активностях</li>
                    <li>Не стесняйтесь задавать вопросы</li>
                </ul>

                <p>Добро пожаловать в семью Eternal!</p>
                ''',
                'category': 'clan'
            },
            {
                'title': 'Гильдейская война - Подготовка к битве',
                'content': '''
                Внимание! В воскресенье состоится гильдейская война против клана "Blood Ravens". Начинаем подготовку!

                <h3>План подготовки:</h3>
                <ul>
                    <li><strong>Пятница:</strong> Стратегическое планирование</li>
                    <li><strong>Суббота:</strong> Тренировочные бои</li>
                    <li><strong>Воскресенье:</strong> Основная битва</li>
                </ul>

                <h3>Требования к участникам:</h3>
                <ul>
                    <li>Уровень 50+</li>
                    <li>Полный набор экипировки</li>
                    <li>Наличие зелий и расходников</li>
                    <li>Обязательное участие в тренировках</li>
                </ul>

                <h3>Награды за победу:</h3>
                <ul>
                    <li>5000 золота каждому участнику</li>
                    <li>Эксклюзивные предметы</li>
                    <li>Повышение репутации клана</li>
                    <li>Специальные достижения</li>
                </ul>

                <p>Регистрация открыта в Discord канале #гильдейские-войны</p>
                ''',
                'category': 'events'
            },
            {
                'title': 'Новые локации в игре - Исследуем вместе!',
                'content': '''
                Разработчики добавили новые захватывающие локации в мир Throne and Liberty!

                <h3>Новые зоны:</h3>
                <ul>
                    <li><strong>Замерзшие пики:</strong> Высокоуровневая зона для 60+ игроков</li>
                    <li><strong>Подземные руины:</strong> Древние катакомбы с сокровищами</li>
                    <li><strong>Плавающий остров:</strong> Уникальная локация с редкими ресурсами</li>
                </ul>

                <h3>Особенности новых зон:</h3>
                <ul>
                    <li>Уникальные боссы и монстры</li>
                    <li>Редкие ресурсы и материалы</li>
                    <li>Скрытые квесты и достижения</li>
                    <li>Специальные события</li>
                </ul>

                <p>Клан организует исследовательские экспедиции в новые зоны. Присоединяйтесь к нам!</p>

                <blockquote>
                    "Новые локации потрясающие! Особенно впечатляют Замерзшие пики с их атмосферой." - @ExplorerPro
                </blockquote>
                ''',
                'category': 'game'
            },
            {
                'title': 'Система достижений - Покажите свои навыки!',
                'content': '''
                В игру добавлена новая система достижений, которая позволит игрокам показать свои навыки и получить уникальные награды.

                <h3>Категории достижений:</h3>
                <ul>
                    <li><strong>PvP достижения:</strong> Победы в боях, убийства боссов</li>
                    <li><strong>Исследовательские:</strong> Открытие новых зон, поиск сокровищ</li>
                    <li><strong>Социальные:</strong> Помощь другим игрокам, участие в событиях</li>
                    <li><strong>Коллекционные:</strong> Сбор редких предметов и ресурсов</li>
                </ul>

                <h3>Награды за достижения:</h3>
                <ul>
                    <li>Уникальные титулы</li>
                    <li>Специальные эффекты персонажа</li>
                    <li>Эксклюзивные предметы</li>
                    <li>Дополнительные слоты инвентаря</li>
                </ul>

                <p>Клан создает команды для выполнения сложных достижений. Присоединяйтесь к нам!</p>
                ''',
                'category': 'updates'
            }
        ]
        
        # Создаем новости с разными датами
        for i, news_item in enumerate(news_data):
            # Создаем дату с разбросом в последние 30 дней
            days_ago = random.randint(0, 30)
            created_date = timezone.now() - timedelta(days=days_ago)
            
            slug = slugify(news_item['title'])
            news, created = News.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': news_item['title'],
                    'content': news_item['content'],
                    'category': news_item['category'],
                    'author': user,
                    'is_published': True,
                    'created_at': created_date,
                    'updated_at': created_date
                }
            )
            
            if created:
                self.stdout.write(f'Создана новость: {news.title}')
        
        # Создаем несколько тестовых членов клана
        clan_members_data = [
            {'username': 'warrior_master', 'game_nickname': 'WarriorMaster', 'role': 'officer', 'level': 55},
            {'username': 'mage_pro', 'game_nickname': 'MagePro', 'role': 'member', 'level': 52},
            {'username': 'healer_queen', 'game_nickname': 'HealerQueen', 'role': 'member', 'level': 50},
            {'username': 'shadow_hunter', 'game_nickname': 'ShadowHunter', 'role': 'recruit', 'level': 45},
            {'username': 'light_mage', 'game_nickname': 'LightMage', 'role': 'recruit', 'level': 42},
        ]
        
        for member_data in clan_members_data:
            member_user, created = User.objects.get_or_create(
                username=member_data['username'],
                defaults={
                    'email': f"{member_data['username']}@eternal-clan.com",
                    'first_name': member_data['game_nickname'],
                    'last_name': 'Clan Member'
                }
            )
            
            if created:
                member_user.set_password('test123')
                member_user.save()
            
            member, created = ClanMember.objects.get_or_create(
                user=member_user,
                defaults={
                    'game_nickname': member_data['game_nickname'],
                    'role': member_data['role'],
                    'level': member_data['level'],
                    'is_approved': True,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Создан член клана: {member.game_nickname}')
        
        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )
        self.stdout.write('Логин: admin, Пароль: admin123') 