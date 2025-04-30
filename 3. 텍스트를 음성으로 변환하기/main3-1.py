from gtts import gTTS
import os
from datetime import datetime

def text_to_speech(text, language='ko', speed=1.2):
    try:
        # gTTS를 사용하여 텍스트를 음성으로 변환
        tts = gTTS(text=text, lang=language, slow=False)
        
        # 현재 날짜와 시간을 파일명에 추가
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"/Users/jeongyong/Desktop/파이썬과 40개의 작품들/3. 텍스트를 음성으로 변환하기/output_{current_time}.mp3"
        tts.save(save_path)
        print(f"텍스트가 음성으로 변환되어 '{save_path}' 파일로 저장되었습니다.")
        
        # 변환된 음성 파일 재생
        os.system(f"start '{save_path}'" if os.name == 'nt' else f"open '{save_path}'")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    text = "안녕하세요, 오늘은 파이썬 프로젝트의 시작일입니다. 먼저 음성 변환 작업을 실험하고 있습니다. 좋은 결과가 있기를"
    text_to_speech(text)

#기초