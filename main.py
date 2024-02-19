import time

from config import settings
from slack_monitor import SlackMonitor

if __name__ == "__main__":
    monitor = SlackMonitor(
        token=settings.SLACK_USER_TOKEN,
        channel_id=settings.SLACK_TARGET_CHANNEL_ID,
    )

    while True:
        if settings.WORKING_HOUR_START <= time.localtime().tm_hour < settings.WORKING_HOUR_END:
            monitor.run(settings.SLACK_USER_ID, last_message_limit=settings.LAST_MESSAGES_LIMIT)

        time.sleep(settings.LOOP_INTERVAL)
