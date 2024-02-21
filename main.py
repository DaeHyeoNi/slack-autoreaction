import time

from config import logging_handler, settings
from modules.slack_monitor import SlackMonitor

logger = logging_handler.get_logger()


def is_weekend(now: time.struct_time):
    # 주말에 실행하도록 설정되어 있다면 항상 True를 반환합니다.
    if not settings.WORKING_DAY_ONLY:
        return True

    return now.tm_wday >= 5


def in_working_time(now: time.struct_time):
    return settings.WORKING_HOUR_START <= now.tm_hour < settings.WORKING_HOUR_END


if __name__ == "__main__":
    logger.info("Start monitoring...")

    monitor = SlackMonitor()
    while True:
        now = time.localtime()
        if not is_weekend(now) and in_working_time(now):
            monitor.run()

        time.sleep(settings.LOOP_INTERVAL)
