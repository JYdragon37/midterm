import pyupbit

# BTC-KRW 시세 가져오기 테스트
def test_pyupbit():
    try:
        # 현재 비트코인 시세 가져오기
        price = pyupbit.get_current_price("KRW-BTC")
        if price is not None:
            print(f"PyUpbit 정상 작동: BTC 현재 시세는 {price:,.0f} 원입니다.")
        else:
            print("PyUpbit 에러: BTC-KRW 데이터를 가져올 수 없습니다.")
    except Exception as e:
        print(f"PyUpbit 에러 발생: {e}")

# 테스트 실행
if __name__ == "__main__":
    test_pyupbit()
