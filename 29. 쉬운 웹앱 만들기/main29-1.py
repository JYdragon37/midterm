import streamlit as st
import pyupbit

# Streamlit 앱 제목
st.title("📈 비트코인 시세 확인")

# BTC 시세 가져오기 함수
def get_btc_price():
    try:
        price = pyupbit.get_current_price("BTC-KRW")
        if price is None:
            raise ValueError("Code not found")  # 시세를 가져오지 못했을 때 오류 발생
        return price
    except Exception as e:
        st.error(f"시세 정보를 가져오는 중 오류 발생: {e}")
        return None

# 시세 가져오기
btc_price = get_btc_price()

# 시세 출력
if btc_price:
    st.metric(label="BTC/KRW 현재 시세", value=f"{btc_price:,.0f} 원")
else:
    st.warning("비트코인 시세 정보를 가져올 수 없습니다.")
