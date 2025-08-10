import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Настраивает и возвращает веб-драйвер Selenium."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Запуск в фоновом режиме
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def find_element_with_fallback(driver, selectors, timeout=15):
    """
    Пытается найти элемент поочередно по нескольким селекторам.
    Возвращает первый найденный элемент.
    """
    wait = WebDriverWait(driver, timeout)
    for selector in selectors:
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            print(f"  ✅ Элемент найден по селектору: '{selector}'")
            return element
        except:
            print(f"  ℹ️ Элемент не найден по селектору: '{selector}'")
    return None

def parse_news():
    """
    Парсит новости с сайта playthroneandliberty.com, переходя на каждую страницу
    для получения полного контента, включая текст и видео.
    """
    URL = "https://www.playthroneandliberty.com/en-us/news"
    base_url = "https://www.playthroneandliberty.com"
    
    driver = setup_driver()
    parsed_data = []

    try:
        # 1. Получаем список новостей с главной страницы
        print(f"🚀 Открытие главной страницы новостей: {URL}")
        driver.get(URL)
        
        wait = WebDriverWait(driver, 20)
        news_container_selector = '#ags-NewsLandingPage-renderBlogList'
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, news_container_selector)))
            print("✅ Страница новостей загружена, парсинг списка...")
        except Exception as e:
            print(f"❌ Не удалось загрузить контейнер новостей '{news_container_selector}'. Ошибка: {e}")
            driver.save_screenshot('debug_screenshot_list.png')
            print("📷 Скриншот сохранен в 'debug_screenshot_list.png'")
            return

        news_list_elements = driver.find_elements(By.CSS_SELECTOR, f'{news_container_selector} .ags-SlotModule--blog')
        
        if not news_list_elements:
            print("⚠️  Не удалось найти новости на странице. Возможно, изменилась структура сайта.")
            return

        # 2. Собираем предварительную информацию о каждой новости
        for news_item_element in news_list_elements:
            try:
                link = news_item_element.find_element(By.CSS_SELECTOR, '.ags-SlotModule-slotLink').get_attribute('href')
                image_url = news_item_element.find_element(By.CSS_SELECTOR, '.ags-SlotModule-slotLink-imageContainer-image').get_attribute('src')

                if link and not link.startswith('http'):
                    link = base_url + link
                if image_url and not image_url.startswith('http'):
                    image_url = 'https:' + image_url
                    
                parsed_data.append({
                    "title": "", "content": "", "category": "",
                    "author": "news_parser", "is_published": True,
                    "source_url": link, "image_url": image_url
                })
            except Exception as e:
                print(f"  ❌ Ошибка при парсинге элемента списка новостей: {e}")

        if not parsed_data:
            print("⚠️  Новости для парсинга не найдены.")
            return

        print(f"✅ Найдено {len(parsed_data)} новостей. Начинаем парсинг полного контента...")

        # 3. Переходим на страницу каждой новости для сбора полного контента
        for i, news_item in enumerate(parsed_data):
            link = news_item.get('source_url')
            if not link:
                print(f"⏩ Пропуск '{news_item.get('title', 'N/A')}' из-за отсутствия URL.")
                continue

            print(f"📰 ({i+1}/{len(parsed_data)}) Парсинг: {link}")
            try:
                driver.get(link)

                # Извлекаем заголовок и категорию со страницы статьи
                try:
                    title = driver.title.split('|')[0].strip()
                    news_item['title'] = title
                    
                    # Пытаемся извлечь категорию из URL
                    url_parts = link.split('/')
                    if len(url_parts) > 4:
                        category = url_parts[-2]
                        # Простая очистка, можно улучшить
                        if 'update' in category:
                            category = 'update'
                        elif 'event' in category:
                            category = 'event'
                        news_item['category'] = category

                    print(f"  - Заголовок: '{title}'")
                    print(f"  - Категория: '{news_item['category']}'")
                except Exception as e:
                    print(f"  ⚠️ Не удалось извлечь заголовок/категорию: {e}")

                # Список селекторов для поиска контейнера статьи
                content_selectors = [
                    'article .ags-rich-text-div',                 # Новый селектор на основе фидбека
                    '.ags-Article-contentRoot .ags-Article-body', # Предполагаемый основной селектор
                    '.ags-Article-contentRoot',                   # Запасной вариант
                    'article.article',                            # Общий тег
                    'div[role="article"]',                        # ARIA role
                    '#main-content',                              # Общий ID
                ]
                
                article_body_element = find_element_with_fallback(driver, content_selectors)
                
                if not article_body_element:
                    raise Exception("Не удалось найти контент статьи ни по одному из селекторов.")

                content_html = article_body_element.get_attribute('outerHTML')
                news_soup = BeautifulSoup(content_html, 'html.parser')

                # Очистка и обработка контента
                for unwanted in news_soup.select('.ags-Article-socialShare, .ags-Article-tags'):
                    unwanted.decompose()

                for img in news_soup.select('img'):
                    src = img.get('src', '')
                    if src and not src.startswith('http'):
                        img['src'] = ('https:' + src) if src.startswith('//') else (base_url + src)

                for iframe in news_soup.select('iframe'):
                    src = iframe.get('src', '')
                    if src and not src.startswith('http'):
                        iframe['src'] = ('https:' + src) if src.startswith('//') else (base_url + src)

                news_item['content'] = str(news_soup)
                print(f"  ✅ Контент успешно получен для '{news_item['title']}'.")

            except Exception as e:
                print(f"  ❌ Ошибка при парсинге страницы '{news_item['title']}': {e}")
                debug_filename = f"debug_article_{i}.html"
                with open(debug_filename, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.save_screenshot(f'debug_article_{i}.png')
                print(f"  📄 HTML и скриншот сохранены для отладки: {debug_filename}, debug_article_{i}.png")
                news_item['content'] = f"<p>Не удалось загрузить контент. <a href='{link}' target='_blank'>Ссылка на источник</a></p>"
            
            time.sleep(1)

    except Exception as e:
        print(f"❌ Произошла критическая ошибка в процессе парсинга: {e}")
    finally:
        driver.quit()

    # 4. Сохраняем результат
    output_file = 'bot_news/parsed_news.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ Парсинг завершен. Результаты сохранены в {output_file}")


if __name__ == '__main__':
    parse_news()
