import qrcode
import os

def generate_qr_code(url, save_path):
    try:
        # 디렉터리 생성
        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # QR 코드 생성
        qr = qrcode.QRCode(
            version=1,  # 버전: QR 코드의 크기를 결정 (1~40)
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # 오류 수정 수준
            box_size=10,  # 각 점의 크기
            border=4  # 경계의 두께
        )
        qr.add_data(url)
        qr.make(fit=True)

        # QR 코드 이미지 생성
        img = qr.make_image(fill='black', back_color='white')
        img.save(save_path)
        print(f"QR 코드가 생성되어 '{save_path}' 파일로 저장되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    urls = [
        ("https://www.naver.com", "/Users/jeongyong/Desktop/파이썬과 40개의 작품들/4. QR코드 생성기/naver_qr_code.png"),
        ("https://www.portal.korea.ac.kr", "/Users/jeongyong/Desktop/파이썬과 40개의 작품들/4. QR코드 생성기/korea_univ_qr_code.png"),
        ("https://www.netflix.com", "/Users/jeongyong/Desktop/파이썬과 40개의 작품들/4. QR코드 생성기/netflix_qr_code.png")
    ]

    for url, save_path in urls:
        generate_qr_code(url, save_path)
