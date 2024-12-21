import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def get_news(filename='latest_news.csv'):
    try:
        sections = {
            '종합': 'all',
            '경제': 'eco',
            'IT': 'its',
            '세계': 'int'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        all_news_items = []

        for section_name, section_code in sections.items():
            url = f"https://news.nate.com/rank/interest?sc={section_code}&p=day"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            limit = 10 if section_code == 'all' else 5
            news_list = soup.select('div.mlt01')[:limit]

            for idx, news in enumerate(news_list, 1):
                link = news.find('a')['href']
                if link.startswith('//'):
                    link = 'https:' + link
                elif not link.startswith('http'):
                    link = 'https://news.nate.com' + link

                title = news.find('h2', class_='tit').text.strip()

                all_news_items.append({
                    'title': title,
                    'link': link,
                    'number': idx,
                    'section': section_name,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        # CSV 파일로 저장 (고정된 파일명 사용)
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Section', 'Number', 'Title', 'Link', 'Timestamp'])
            for news in all_news_items:
                writer.writerow([
                    news['section'],
                    news['number'],
                    news['title'],
                    news['link'],
                    news['timestamp']
                ])

        return all_news_items
    except Exception as e:
        print(f"뉴스를 불러오는데 실패했습니다: {str(e)}")
        return []