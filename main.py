import time

from config import logging_handler, settings
from modules.slack_monitor import SlackMonitor

logger = logging_handler.get_logger()


def is_weekend():
    # 주말에 실행하도록 설정되어 있다면 항상 True를 반환합니다.
    if not settings.WORKING_DAY_ONLY:
        return True

    return time.localtime().tm_wday >= 5

def in_working_time():
    return settings.WORKING_HOUR_START <= time.localtime().tm_hour < settings.WORKING_HOUR_END


if __name__ == "__main__":
    monitor = SlackMonitor(
        token=settings.SLACK_USER_TOKEN,
        channel_id=settings.SLACK_TARGET_CHANNEL_ID,
    )

    logger.info("Start monitoring...")

    while True:
        if not is_weekend() and in_working_time:
            monitor.run(settings.SLACK_USER_ID, last_message_limit=settings.LAST_MESSAGES_LIMIT)

        time.sleep(settings.LOOP_INTERVAL)
