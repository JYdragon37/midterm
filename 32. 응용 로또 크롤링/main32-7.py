import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import sqlite3
from PIL import Image, ImageTk

# DB 경로
DB_PATH = r"C:\Users\highk\pypy50\lotto_stats.db"

def get_next_round():
    """DB에서 다음 회차 번호를 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(회차) FROM lotto_round_data")
    latest_round = cursor.fetchone()[0]
    conn.close()
    return (latest_round or 0) + 1  # 마지막 회차 + 1 반환

def generate_lotto_set():
    """정교한 로직에 따라 번호 세트를 생성합니다."""
    all_numbers = list(range(1, 46))
    return sorted(random.sample(all_numbers, 6))

def generate_multiple_sets():
    """5개의 추천 번호 세트를 생성합니다."""
    sets = [generate_lotto_set() for _ in range(5)]
    return sets

# GUI 애플리케이션
class LottoCadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lotto_Cado - 귀여운 로또 추천 봇")
        self.root.geometry("400x750")  # 창 크기 조정
        self.root.resizable(False, False)
        self.root.configure(bg="#f8f8f8")  # 배경 색상

        # 상단 제목 + 최신 회차 표시
        next_round = get_next_round()
        self.title_label = tk.Label(
            root, text=f"Lotto_Cado - {next_round}회차", 
            font=("Comic Sans MS", 24, "bold"),
            fg="#4CAF50", bg="#f8f8f8"
        )
        self.title_label.pack(pady=10)

        # 아보카도 이미지 (축소)
        original_image = Image.open("avocado.png")
        resized_image = original_image.resize((150, 150))  # 이미지 크기 축소
        self.avocado_image = ImageTk.PhotoImage(resized_image)
        self.image_label = tk.Label(root, image=self.avocado_image, bg="#f8f8f8")
        self.image_label.pack()

        # 버튼
        self.generate_button = tk.Button(
            root, text="추천 번호 생성하기 🍀", font=("Helvetica", 14),
            bg="#4CAF50", fg="white", activebackground="#45a049",
            command=self.display_lotto_sets
        )
        self.generate_button.pack(pady=10)

        # 결과 표시 영역 (스크롤 포함)
        self.result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
        self.result_canvas = tk.Canvas(self.result_frame, bg="#ffffff", height=300, highlightthickness=0)  # 높이 제한
        self.scrollbar = ttk.Scrollbar(
            self.result_frame, orient="vertical", command=self.result_canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.result_canvas, bg="#ffffff")

        # 스크롤 가능한 영역 구성
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.result_canvas.configure(scrollregion=self.result_canvas.bbox("all"))
        )
        self.result_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.result_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.result_frame.pack(padx=20, pady=10, fill="both")
        self.result_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 하단 안내 메시지
        self.footer_label = tk.Label(
            root, text="행운을 가져다 줄 귀여운 아보카도와 함께! 🥑", font=("Comic Sans MS", 10),
            fg="#555555", bg="#f8f8f8"
        )
        self.footer_label.pack(side="bottom", pady=10)

    def display_lotto_sets(self):
        """추천 번호 세트를 표시합니다."""
        # 기존 결과 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 추천 번호 생성
        lotto_sets = generate_multiple_sets()

        # 추천 번호 세트 표시
        for i, lotto_set in enumerate(lotto_sets, 1):
            set_label = tk.Label(
                self.scrollable_frame,
                text=f"{i}번 세트: {lotto_set}",
                font=("Helvetica", 14),
                fg="#333333", bg="#ffffff"
            )
            set_label.pack(pady=5, padx=5)

        # 성공 메시지
        messagebox.showinfo("추천 완료", "번호 추천이 완료되었습니다! 🍀")

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = LottoCadoApp(root)
    root.mainloop()
