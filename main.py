import time

from config import settings
from monitor import SlackMonitor

if __name__ == "__main__":
    monitor = SlackMonitor(
        token=settings.SLACK_USER_TOKEN,
        channel_id=settings.SLACK_TARGET_CHANNEL_ID,
    )

    last_message_limit = 3  # 최근 3개의 메시지만 확인

    while True:
        if settings.WORKING_HOUR_START <= time.localtime().tm_hour < settings.WORKING_HOUR_END:
            monitor.run(settings.SLACK_USER_ID, last_message_limit=settings.LAST_MESSAGES_LIMIT)

        time.sleep(settings.LOOP_INTERVAL)
