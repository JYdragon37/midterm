import requests
from bs4 import BeautifulSoup

def get_top_10_news():
    # 네이트 뉴스 랭킹 URL
    url = "https://news.nate.com/rank/interest?sc=all&p=day&date={today}"
    
    # HTTP 요청 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 웹페이지 가져오기
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 뉴스 아이템을 저장할 리스트
    news_items = []

    # 1-5위 뉴스 찾기
    news_list_1_5 = soup.select('div.mlt01')[:5]
    for news in news_list_1_5:
        link = news.find('a')['href']
        if link.startswith('//'):  # URL이 //로 시작하면
            link = 'https:' + link  # https: 만 추가
        elif not link.startswith('http'):  # 그 외의 상대 경로인 경우
            link = 'https://news.nate.com' + link
        title = news.find('h2', class_='tit').text.strip()
        news_items.append({
            'title': title,
            'link': link
        })

    # 6-10위 뉴스 찾기 (다른 형식)
    news_list_6_10 = soup.select('dl.mduRank')[5:10]
    for dl in news_list_6_10:
        next_a = dl.find_next_sibling('a')
        if next_a:
            link = next_a['href']
            if link.startswith('//'):  # URL이 //로 시작하면
                link = 'https:' + link  # https: 만 추가
            elif not link.startswith('http'):  # 그 외의 상대 경로인 경우
                link = 'https://news.nate.com' + link
            title = next_a.find('h2').text.strip()
            news_items.append({
                'title': title,
                'link': link
            })

    return news_items

if __name__ == "__main__":
    news_items = get_top_10_news()
    
    # HTML 형식으로 출력
    for i, news in enumerate(news_items, 1):
        print(f"{i}. <a href='{news['link']}'>{news['title']}</a>")
