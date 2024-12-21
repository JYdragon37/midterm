import requests
import urllib.parse

# 네이버 API 키
client_id = 'Bs4d81MbFjUn7Mfc2oO5'
client_secret = 'NvF9NY3CPs'

# 검색 키워드와 API URL
query = urllib.parse.quote("여의도 맛집")
url = f"https://openapi.naver.com/v1/search/blog.json?query={query}&display=10&start=1&sort=sim"

# 요청 헤더
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# API 호출
response = requests.get(url, headers=headers)

# 결과 출력
if response.status_code == 200:
    data = response.json()
    for item in data['items']:
        print(f"Title: {item['title']}, Link: {item['link']}")
else:
    print(f"Error Code: {response.status_code}")
