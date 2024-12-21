import streamlit as st
import pyupbit
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams

# 1) 한글 폰트 지원
rcParams['font.family'] = 'Malgun Gothic'  # Windows 환경: 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 음수 표시 지원

# Streamlit 앱 제목
st.title("📈 비트코인 시세 확인: 기간별 그래프")

# 4) 최근 7일 기본값으로 설정
start_date, end_date = st.date_input(
    "기간을 선택하세요",
    value=[date.today() - timedelta(days=7), date.today()],  # 기본값: 최근 7일
    min_value=date(2021, 1, 1),  # 최소 날짜
    max_value=date.today()  # 최대 날짜
)

# 선택한 기간 출력
st.write(f"선택한 기간: {start_date} ~ {end_date}")

# 선택한 기간의 비트코인 데이터 가져오기 함수
def get_btc_data(start_date, end_date):
    try:
        # PyUpbit에서 데이터 가져오기 (일간 데이터)
        df = pyupbit.get_ohlcv("KRW-BTC", interval="day")
        filtered_df = df.loc[start_date:end_date]
        return filtered_df
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류 발생: {e}")
        return None

# 데이터 가져오기
btc_data = get_btc_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

# 그래프와 수익률 계산
if btc_data is not None and not btc_data.empty:
    # 시작가와 종료가를 가져와 수익률 계산
    start_price = btc_data["close"].iloc[0]
    end_price = btc_data["close"].iloc[-1]
    return_rate = ((end_price - start_price) / start_price) * 100

    # 3) 우상단에 퍼센티지 박스 표시
    st.markdown(
        f"""
        <div style="text-align:right; padding:10px; background-color:#f0f0f0; border-radius:5px; font-size:18px; color:#000;">
        <b>기간 수익률:</b> {return_rate:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )

    # 그래프 그리기 (Matplotlib 사용)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(btc_data.index, btc_data["close"], label="종가", color="blue", linewidth=2)

    # 그래프 스타일 설정
    ax.set_ylim(30000000, btc_data["close"].max() * 1.1)  # 최소값 3천만 원, 최대값 10% 여유
    ax.set_title("BTC/KRW 기간별 종가", fontsize=16)
    ax.set_xlabel("날짜", fontsize=12)
    ax.set_ylabel("가격 (KRW)", fontsize=12)
    ax.grid(color='lightgray', linestyle='--', linewidth=0.5)  # 연한 격자 추가
    ax.legend()

    # X축 날짜 형식 조정
    fig.autofmt_xdate(rotation=45)

    # 2) Y축 금액 단위를 숫자만 표시
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

    # Streamlit에 그래프 표시
    st.pyplot(fig)
else:
    st.warning("선택한 기간에 해당하는 데이터를 가져올 수 없습니다.")
