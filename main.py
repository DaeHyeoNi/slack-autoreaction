import time

from config import settings
from modules.slack_monitor import SlackMonitor


def is_weekend():
    current_day = time.localtime().tm_wday
    return current_day >= 5


if __name__ == "__main__":
    monitor = SlackMonitor(
        token=settings.SLACK_USER_TOKEN,
        channel_id=settings.SLACK_TARGET_CHANNEL_ID,
    )

    while True:
        current_day = time.localtime().tm_wday
        if not is_weekend() and settings.WORKING_HOUR_START <= time.localtime().tm_hour < settings.WORKING_HOUR_END:
            monitor.run(settings.SLACK_USER_ID, last_message_limit=settings.LAST_MESSAGES_LIMIT)

        time.sleep(settings.LOOP_INTERVAL)
