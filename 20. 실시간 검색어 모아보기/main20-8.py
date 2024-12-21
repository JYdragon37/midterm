import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Signal.bz 뉴스 페이지에서 실시간 검색어 10가지를 가져오기
URL = "https://signal.bz/news"

# 실시간 검색어 가져오기 함수
def get_realtime_search_terms(url):
    print(f"[{datetime.datetime.now()}] 실시간 검색어 수집을 시작합니다.")
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청이 성공적으로 이루어졌는지 확인

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 실시간 검색어 요소 선택 (CSS Selector 사용)
        search_elements = soup.select("span.rank-text")
        terms = [element.text.strip() for element in search_elements[:10]]

        if terms:
            print(f"[{datetime.datetime.now()}] 실시간 검색어 수집 성공: {terms}")
        else:
            print(f"[{datetime.datetime.now()}] 실시간 검색어를 수집하지 못했습니다.")
        return terms
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 실시간 검색어 수집 중 오류 발생: {e}")
        return []

# 인기 뉴스 가져오기 함수
def get_popular_news(url):
    print(f"[{datetime.datetime.now()}] 인기 뉴스 수집을 시작합니다.")
    try:
        response = requests.get(url)
        response.raise_for_status()

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 인기 뉴스 요소 선택 (CSS Selector 사용)
        popular_news_elements = soup.select("div.title")
        popular_news = [element.text.strip() for element in popular_news_elements[:10]]

        if popular_news:
            print(f"[{datetime.datetime.now()}] 인기 뉴스 수집 성공: {popular_news}")
        else:
            print(f"[{datetime.datetime.now()}] 인기 뉴스를 수집하지 못했습니다.")
        return popular_news
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 인기 뉴스 수집 중 오류 발생: {e}")
        return []

# 검색어 출력 및 저장 함수
def save_search_terms(terms, popular_news):
    print(f"[{datetime.datetime.now()}] 검색어 및 인기 뉴스 저장을 시작합니다.")
    current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if terms:
        df = pd.DataFrame(terms, columns=['실시간 검색어'])
        filename = f"실검top10_{current_date}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"검색어가 파일로 저장되었습니다: {filename}")
        print(df)
    else:
        print("검색어를 가져올 수 없습니다.")

    if popular_news:
        df_popular = pd.DataFrame(popular_news, columns=['인기 뉴스'])
        filename_popular = f"인기뉴스_{current_date}.csv"
        df_popular.to_csv(filename_popular, index=False, encoding='utf-8-sig')
        print(f"인기 뉴스가 파일로 저장되었습니다: {filename_popular}")
        print(df_popular)
    else:
        print("인기 뉴스를 가져올 수 없습니다.")

# 메인 함수
if __name__ == "__main__":
    terms = get_realtime_search_terms(URL)
    popular_news = get_popular_news(URL)
    save_search_terms(terms, popular_news)
