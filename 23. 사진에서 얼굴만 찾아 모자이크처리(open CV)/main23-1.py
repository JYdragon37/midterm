import cv2
import os

# 이미지 경로 설정
image_path = r'C:\Users\highk\pypy50\sample1.jpg'

# Haar Cascade 파일의 경로 설정 (해당 파일을 로컬 프로젝트 경로에 저장하세요)
haarcascade_path = r'C:\Users\highk\pypy50\haarcascade_frontalface_default.xml'

# 모자이크 비율 설정 (작을수록 모자이크가 강해짐, 클수록 약해짐)
mosaic_ratio = 5  # 이 값을 조정하여 모자이크 정도를 변경하세요

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

        # 얼굴 인식용 CascadeClassifier 생성
        if not os.path.exists(haarcascade_path):
            print(f"Haar Cascade 파일이 존재하지 않습니다. 경로를 확인해 주세요: {haarcascade_path}")
        else:
            face_cascade = cv2.CascadeClassifier(haarcascade_path)

            # 이미지 그레이스케일 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 얼굴 검출
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # 얼굴 모자이크 처리
            for (x, y, w, h) in faces:
                # 얼굴 영역 추출
                face = image[y:y+h, x:x+w]
                # 얼굴 영역 모자이크 처리 (이미지 축소 후 확대)
                face = cv2.resize(face, (w // mosaic_ratio, h // mosaic_ratio), interpolation=cv2.INTER_LINEAR)
                face = cv2.resize(face, (w, h), interpolation=cv2.INTER_NEAREST)
                # 모자이크 처리된 얼굴을 원래 이미지에 적용
                image[y:y+h, x:x+w] = face

            # 결과 이미지 창에 표시
            cv2.imshow('Mosaic Image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
