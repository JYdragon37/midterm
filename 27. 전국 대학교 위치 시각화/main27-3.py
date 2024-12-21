import pandas as pd
import requests
import re

# VWorld API URL 및 인증키
api_url = "https://api.vworld.kr/req/address?"
api_key = "94194597-6426-3593-8432-EEC2386EDD20"  # 발급받은 API Key 입력

# 파일 경로 설정 (입력 데이터)
file_path = r"C:\Users\highk\pypy50\27. 전국 대학교 위치 시각화\고등교육기관 하반기 주소록(2023).xlsx"

# Excel 파일 읽기
df = pd.read_excel(file_path, header=5)

# 필요한 열만 선택 (학교명과 주소)
school_data = df[['학교명', '주소']]

# 결과 저장
coordinates = []

for _, row in school_data.iterrows():
    school_name = row['학교명']
    address = row['주소']

    # **괄호 제거 및 간소화**
    simplified_address = re.sub(r'\(.*?\)', '', address).strip()

    # 좌표를 찾았는지 여부 확인
    found = False

    for address_type in ["ROAD", "PARCEL"]:  # 도로명주소 → 지번주소 순서로 시도
        if found:
            break  # 좌표를 찾았으면 추가 요청 중단

        params = {
            "service": "address",
            "request": "getCoord",
            "key": api_key,
            "address": simplified_address,
            "type": address_type,
            "format": "json",
            "crs": "epsg:4326"
        }

        # API 요청
        response = requests.get(api_url, params=params)
        print(f"요청 URL ({address_type}): {response.url}")  # 디버깅용 URL 출력

        if response.status_code == 200:
            data = response.json()
            if data['response']['status'] == 'OK':
                # 좌표 추출
                x = data['response']['result']['point']['x']  # 경도
                y = data['response']['result']['point']['y']  # 위도
                coordinates.append({
                    "학교명": school_name,
                    "주소": address,
                    "유형": address_type,
                    "경도": x,
                    "위도": y
                })
                found = True  # 좌표를 찾았음을 표시
            else:
                print(f"주소 '{simplified_address}'에 대한 검색 결과가 없습니다. (타입: {address_type})")
        else:
            print(f"API 요청 실패: {response.status_code}")

    # 검색 결과가 없을 경우 None 추가
    if not found:
        coordinates.append({
            "학교명": school_name,
            "주소": address,
            "유형": None,
            "경도": None,
            "위도": None
        })

# 결과를 Pandas DataFrame으로 변환
df_coordinates = pd.DataFrame(coordinates)

# 좌표가 있는 주소만 필터링
df_valid = df_coordinates.dropna(subset=["경도", "위도"])

# 데이터 확인
print("\n=== 좌표 데이터 ===")
print(df_valid)

# CSV로 저장 (옵션)
output_path = r"C:\Users\highk\pypy50\27. 전국 대학교 위치 시각화\대학_주소_좌표.csv"
df_valid.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n결과가 '{output_path}' 파일에 저장되었습니다.")
