from googletrans import Translator

def translate_text():
    # Translator 객체 생성
    translator = Translator()
    
    # 번역할 텍스트 입력받기
    text = input("번역할 텍스트를dh 입력하세요: ")
    
    # 대상 언어 입력받기 (예: 'en' -> 영어, 'ko' -> 한국어 등)
    target_language = input("번역할 대상 언어 코드를 입력하세요 (예: 'en' for English, 'ko' for Korean): ")
    
    try:
        # 번역 실행
        translated = translator.translate(text, dest=target_language)
        
        # 번역 결과 출력
        print(f"번역 결과: {translated.text}")
    except Exception as e:
        print(f"번역 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    translate_text()

#기초