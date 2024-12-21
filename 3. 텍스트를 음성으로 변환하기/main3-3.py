from gtts import gTTS
import os
from datetime import datetime

def text_to_speech_from_file(file_path, language='ko'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().strip()
            if not text:
                raise ValueError("No text to speak")
            # gTTS를 사용하여 텍스트를 음성으로 변환
            tts = gTTS(text=text, lang=language, slow=False)
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

            save_path = f"/Users/jeongyong/Desktop/파이썬과 40개의 작품들/3. 텍스트를 음성으로 변환하기/output_{current_time}.mp3"
            tts.save(save_path)
            print(f"텍스트가 음성으로 변환되어 '{save_path}' 파일로 저장되었습니다.")
            
            # 변환된 음성 파일 재생
            os.system(f"start '{save_path}'" if os.name == 'nt' else f"open '{save_path}'")
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except ValueError as ve:
        print(f"오류가 발생했습니다: {ve}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    file_path = "/Users/jeongyong/Desktop/파이썬과 40개의 작품들/3. 텍스트를 음성으로 변환하기/나의텍스트.txt"
    text_to_speech_from_file(file_path)
