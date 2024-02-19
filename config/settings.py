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
SLACK_MYTEAM_ID = os.getenv("SLACK_MYTEAM_ID")

EMOJI_MENTION_IN_CHANNEL_ALL_USERS = os.getenv("EMOJI_MENTION_IN_CHANNEL_ALL_USERS", "nep")
EMOJI_MENTION_TO_ME = os.getenv("EMOJI_MENTION_TO_ME", "nep")
EMOJI_MENTION_TO_MY_TEAM = os.getenv("EMOJI_MENTION_TO_MY_TEAM", "eyes")

NEED_REACTION_COUNT = int(os.getenv("NEED_REACTION_COUNT", 3))
LAST_MESSAGES_LIMIT = int(os.getenv("LAST_MESSAGES_LIMIT", 3))

LOOP_INTERVAL = int(os.getenv("LOOP_INTERVAL", 300))

REPORT_RESULT_TO_DM = get_env_type_boolean("REPORT_RESULT_TO_DM", True)
