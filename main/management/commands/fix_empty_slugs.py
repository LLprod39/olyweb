from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import News


class Command(BaseCommand):
    help = 'Исправляет пустые slug\'ы в модели News'

    def handle(self, *args, **options):
        news_with_empty_slugs = News.objects.filter(slug='')
        
        if not news_with_empty_slugs.exists():
            self.stdout.write(
                self.style.SUCCESS('Нет записей с пустыми slug\'ами')
            )
            return
        
        self.stdout.write(f'Найдено {news_with_empty_slugs.count()} записей с пустыми slug\'ами')
        
        for news in news_with_empty_slugs:
            old_slug = news.slug
            news.slug = slugify(news.title)
            news.save()
            
            self.stdout.write(
                f'Исправлен slug для "{news.title}": "{old_slug}" -> "{news.slug}"'
            )
        
        self.stdout.write(
            self.style.SUCCESS('Все пустые slug\'ы исправлены!')
        ) 