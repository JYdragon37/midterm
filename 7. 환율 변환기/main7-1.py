import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_weekly_usd_to_krw():
    today = datetime.now()
    base_url = "https://www.investing.com/currencies/usd-krw-historical-data"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.investing.com/',
        'Connection': 'keep-alive'
    }
    session = requests.Session()
    session.headers.update(headers)

    for i in range(7):
        day = today - timedelta(days=i)
        try:
            response = session.get(base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'historicalTbl'})
            rows = table.find_all('tr')[1:]
            
            for row in rows:
                columns = row.find_all('td')
                date_str = columns[0].text.strip()
                rate_str = columns[1].text.strip().replace(',', '')
                date_obj = datetime.strptime(date_str, '%b %d, %Y')

                if date_obj.date() == day.date():
                    rate = float(rate_str)
                    print(f"{day.strftime('%Y-%m-%d')}: 1 USD = {rate:.2f} KRW")
                    break
        except Exception as e:
            print(f"{day.strftime('%Y-%m-%d')}: 환율 데이터를 가져올 수 없습니다. 오류: {e}")

if __name__ == "__main__":
    get_weekly_usd_to_krw()
