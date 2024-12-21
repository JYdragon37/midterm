import cv2
import os
import numpy as np
from PIL import Image, ImageFilter

def apply_sketch_effect(image, level):
    # OpenCV 이미지 형식을 PIL 이미지 형식으로 변환
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # 그림 효과 적용 (엣지 강조 필터 사용, level 값으로 강도 조절)
    sketch_image = pil_image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    for _ in range(level):
        sketch_image = sketch_image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    return sketch_image

# 트랙바 콜백 함수
def on_trackbar(val):
    global previous_level
    if val == 0:
        cv2.imshow('Sketch Image', image)  # 원본 이미지 표시
    else:
        sketch_level = int(val * 0.1)  # 트랙바 값의 10%로 변환하여 점진적으로 변경
        sketch_image = apply_sketch_effect(image, sketch_level)
        sketch_image_cv = cv2.cvtColor(np.array(sketch_image), cv2.COLOR_RGB2BGR)
        cv2.imshow('Sketch Image', sketch_image_cv)
    previous_level = val

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

        # 트랙바를 이용하여 그림 효과 강도 조절
        cv2.namedWindow('Sketch Image')
        cv2.createTrackbar('Level', 'Sketch Image', 0, 50, on_trackbar)  # 최대 값을 100으로 증가하여 미세하게 조정 가능

        # 초기 이미지 표시 (원본 이미지)
        cv2.imshow('Sketch Image', image)
        previous_level = 0

        # 사용자가 ESC 키를 누를 때까지 대기
        while True:
            key = cv2.waitKey(1)
            if key == 27:  # ESC 키
                break
            if cv2.getWindowProperty('Sketch Image', cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()
