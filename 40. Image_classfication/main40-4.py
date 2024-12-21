import face_recognition
import os
import shutil
from tqdm import tqdm
import random
import numpy as np

def create_directories(base_dir):
    """분류될 디렉토리 생성"""
    categories = ['test_couple_only', 'test_group_with_couple', 'test_landscape', 'test_others']
    for category in categories:
        category_path = os.path.join(base_dir, category)
        os.makedirs(category_path, exist_ok=True)

def load_known_faces(faces_dir):
    """신랑신부 얼굴 특징을 로드하는 함수"""
    known_encodings = []
    
    print("Loading reference faces...")
    files = [f for f in os.listdir(faces_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    for filename in tqdm(files):
        image_path = os.path.join(faces_dir, filename)
        # 이미지 로드
        image = face_recognition.load_image_file(image_path)
        
        # 얼굴 위치 검출
        face_locations = face_recognition.face_locations(image, model="cnn")
        if not face_locations:
            continue
            
        # 얼굴 특징 추출
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if face_encodings:
            known_encodings.append(face_encodings[0])
    
    print(f"Loaded {len(known_encodings)} reference faces")
    return known_encodings

def classify_image(image_path, known_encodings, tolerance=0.6):
    """이미지 분류 함수"""
    try:
        # 이미지 로드
        image = face_recognition.load_image_file(image_path)
        
        # 얼굴 검출
        face_locations = face_recognition.face_locations(image, model="cnn")
        
        if not face_locations:
            return 'test_landscape'
            
        # 검출된 얼굴들의 특징 추출
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # 신랑신부 얼굴 찾기
        couple_found = False
        for face_encoding in face_encodings:
            # 모든 기준 얼굴과 비교
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
            if True in matches:
                couple_found = True
                break
        
        # 분류 로직
        if couple_found:
            if len(face_locations) <= 2:
                return 'test_couple_only'
            else:
                return 'test_group_with_couple'
        else:
            return 'test_others'
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return 'test_others'

def main():
    # 기본 디렉토리 설정
    base_dir = r"C:\Users\highk\pypy50\40. Image_classfication"
    faces_dir = os.path.join(base_dir, "user_faces")
    wedding_dir = os.path.join(base_dir, "wedding_images")
    
    # 디렉토리 존재 확인
    if not os.path.exists(faces_dir) or not os.path.exists(wedding_dir):
        print("Directories not found!")
        return
    
    # 분류 디렉토리 생성
    create_directories(base_dir)
    
    # 신랑신부 얼굴 특징 로드
    known_encodings = load_known_faces(faces_dir)
    
    if not known_encodings:
        print("No reference faces loaded!")
        return
    
    # 30개의 랜덤 이미지 선택
    all_images = [f for f in os.listdir(wedding_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    sample_images = random.sample(all_images, min(30, len(all_images)))
    
    print("\nClassifying images...")
    for filename in tqdm(sample_images):
        image_path = os.path.join(wedding_dir, filename)
        category = classify_image(image_path, known_encodings)
        destination = os.path.join(base_dir, category, filename)
        shutil.copy2(image_path, destination)
    
    # 결과 출력
    print("\nClassification Results:")
    categories = ['test_couple_only', 'test_group_with_couple', 'test_landscape', 'test_others']
    for category in categories:
        category_path = os.path.join(base_dir, category)
        count = len(os.listdir(category_path))
        print(f"{category}: {count} images")

if __name__ == "__main__":
    main()