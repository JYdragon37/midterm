import os
from PIL import Image
from facenet_pytorch import MTCNN
import torch  # torch 임포트

# 1. 경로 설정
input_folder = r"C:\Users\highk\pypy50\40. 이미지 분류 - 파이토치\image"
output_folder = r"C:\Users\highk\pypy50\40. 이미지 분류 - 파이토치\classified"

# 결과 저장 폴더 생성
os.makedirs(os.path.join(output_folder, "풍경"), exist_ok=True)
os.makedirs(os.path.join(output_folder, "인물"), exist_ok=True)

# 2. MTCNN 초기화
device = "cpu"  # GPU가 없으므로 CPU 사용
mtcnn = MTCNN(keep_all=True, device=device)

# 3. 분류 함수
def classify_image(img_path):
    # 이미지 로드
    img = Image.open(img_path).convert("RGB")
    
    # 이미지 크기 조정 (가로 800px 기준)
    max_width = 800
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)  # LANCZOS 사용
    
    # 얼굴 감지
    boxes, _ = mtcnn.detect(img)
    
    # 얼굴이 감지되면 "인물", 아니면 "풍경"으로 분류
    if boxes is not None:
        return "인물", img
    else:
        return "풍경", img

# 4. 이미지 파일 검색 및 분류
from glob import glob

image_files = glob(f"{input_folder}/*.*")
for img_path in image_files:
    try:
        label, processed_img = classify_image(img_path)
        dest_folder = os.path.join(output_folder, label)
        
        # 결과 저장
        img_name = os.path.basename(img_path)
        dest_path = os.path.join(dest_folder, img_name)
        processed_img.save(dest_path)  # 조정된 이미지 저장
        print(f"Processed: {img_path} -> {dest_path}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

print("모든 이미지 분류 완료!")
