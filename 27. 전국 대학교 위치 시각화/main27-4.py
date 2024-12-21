import pandas as pd
import folium

# CSV 파일 읽기
csv_file = "C:\\Users\\highk\\pypy50\\27. 전국 대학교 위치 시각화\\대학_주소_좌표.csv"
data = pd.read_csv(csv_file, encoding="utf-8")

# 지도 생성 (중심 좌표는 위도와 경도의 평균값 기준)
map = folium.Map(location=[data["위도"].mean(), data["경도"].mean()], zoom_start=10)

# 데이터프레임의 각 행에 대해 마커 추가
for _, row in data.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=row["학교명"],  # 마커 클릭 시 학교명 팝업
        tooltip=row["학교명"]  # 마커 위에 마우스를 올릴 때 학교명 툴팁
    ).add_to(map)

# 지도 저장
output_file = "C:\\Users\\highk\\pypy50\\27. 전국 대학교 위치 시각화\\map_with_markers.html"
map.save(output_file)

print(f"지도 파일이 '{output_file}'에 저장되었습니다.")
