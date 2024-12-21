import cv2
import os
import numpy as np
from PIL import Image, ImageFilter

# 이미지 경로 설정
image_path = r'C:\Users\highk\pypy50\sample1.jpg'

# 이미지 파일이 존재하는지 확인
if not os.path.exists(image_path):
    print(f"이미지 파일이 존재하지 않습니다. 경로를 확인해 주세요: {image_path}")
else:
    # 이미지 로드
    image = cv2.imread(image_path)

    # 이미지가 제대로 로드되었는지 확인
    if image is None:
        print(f"이미지 파일을 열 수 없습니다. 경로를 확인해 주세요: {image_path}")
    else:
        print("이미지 파일이 성공적으로 로드되었습니다.")

        # OpenCV 이미지 형식을 PIL 이미지 형식으로 변환
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # 그림 효과 적용 (엣지 강조 필터 사용)
        sketch_image = pil_image.filter(ImageFilter.CONTOUR)

        # 결과 이미지 창에 표시
        sketch_image.show()

        # 결과 이미지 저장
        sketch_image_path = os.path.join(os.path.dirname(image_path), 'sketch_sample1.jpg')
        sketch_image.save(sketch_image_path)
        print(f"그림 효과가 적용된 이미지가 저장되었습니다: {sketch_image_path}")
