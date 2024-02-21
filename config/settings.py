import os


def get_env_type_boolean(env: str, default=False) -> bool:
    default = "true" if default else "false"
    return os.getenv(env, default).lower() in ("true", "1")


DRY_RUN = get_env_type_boolean("DRY_RUN", True)

LAST_MESSAGES_LIMIT = int(os.getenv("LAST_MESSAGES_LIMIT", 3))

LOOP_INTERVAL = int(os.getenv("LOOP_INTERVAL", 300))

WORKING_HOUR_START = int(os.getenv("WORKING_HOUR_START", 10))
WORKING_HOUR_END = int(os.getenv("WORKING_HOUR_END", 19))

WORKING_DAY_ONLY = get_env_type_boolean("WORKING_DAY_ONLY", True)

SLACK_USER_TOKEN = os.getenv("SLACK_USER_TOKEN")
assert SLACK_USER_TOKEN.startswith("xoxp-"), "User token should start with xoxp-"

# Check for User ID reacted to the message
SLACK_USER_ID = os.getenv("SLACK_USER_ID")
assert SLACK_USER_ID.startswith("U"), "SLACK_USER_ID should start with U"

# Check for Channel ID to monitor
SLACK_TARGET_CHANNEL_ID = os.getenv("SLACK_TARGET_CHANNEL_ID")
assert SLACK_TARGET_CHANNEL_ID.startswith("C"), "SLACK_TARGET_CHANNEL_ID should start with C"

SLACK_MYTEAM_ID = os.getenv("SLACK_MYTEAM_ID")

NEED_REACTION_COUNT = int(os.getenv("NEED_REACTION_COUNT", 5))

EMOJI_MENTION_IN_CHANNEL_ALL_USERS = os.getenv("EMOJI_MENTION_IN_CHANNEL_ALL_USERS", "nep")
EMOJI_MENTION_TO_ME = os.getenv("EMOJI_MENTION_TO_ME", "nep")
EMOJI_MENTION_TO_MY_TEAM = os.getenv("EMOJI_MENTION_TO_MY_TEAM", "eyes")

REPORT_RESULT_TO_DM = get_env_type_boolean("REPORT_RESULT_TO_DM", True)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if REPORT_RESULT_TO_DM:
    assert SLACK_BOT_TOKEN.startswith("xoxb-"), "Bot token should start with xoxb-"
