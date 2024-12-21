from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from pytz import timezone
from modules.news import get_news
from modules.trending import get_trending
from modules.weather import capture_weather

def should_update():
    # 한국 시간 확인
    kr_time = datetime.now(timezone('Asia/Seoul'))
    hour = kr_time.hour
    # 0시~5시59분까지는 업데이트 하지 않음
    return not (0 <= hour < 6)

def update_data():
    if should_update():
        # 뉴스 데이터 업데이트
        get_news(filename='latest_news.csv')
        # 트렌드 데이터 업데이트
        get_trending(filename='latest_trends.csv')
        # 날씨 스크린샷 업데이트
        capture_weather()

def start_scheduler():
    # 서버 시작시 즉시 한 번 실행
    update_data()

    # 이후 스케줄링 시작
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        update_data,
        trigger=CronTrigger(minute=0)  # 매시 정각마다 실행
    )
    scheduler.start()