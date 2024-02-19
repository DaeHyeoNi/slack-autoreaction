import os


def get_env_type_boolean(env: str, default=False) -> bool:
    default = "true" if default else "false"
    return os.getenv(env, default).lower() in ("true", "1")


DRY_RUN = get_env_type_boolean("DRY_RUN", True)
WORKING_HOUR_START = int(os.getenv("WORKING_HOUR_START"))
WORKING_HOUR_END = int(os.getenv("WORKING_HOUR_END"))

SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")
SLACK_USER_ID = os.getenv("SLACK_USER_ID")
SLACK_TARGET_CHANNEL_ID = os.getenv("SLACK_TARGET_CHANNEL_ID")

NEED_REACTION_COUNT = int(os.getenv("NEED_REACTION_COUNT", 3))
LAST_MESSAGES_LIMIT = int(os.getenv("LAST_MESSAGES_LIMIT", 3))

LOOP_INTERVAL = int(os.getenv("LOOP_INTERVAL", 60))