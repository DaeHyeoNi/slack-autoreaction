from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import logging_handler, settings

logger = logging_handler.get_logger()


class SlackMonitor:
    def __init__(self):
        self.slack_client = WebClient(token=settings.SLACK_USER_TOKEN)
        self.slack_bot_client = WebClient(token=settings.SLACK_BOT_TOKEN)
        self.channel_id = settings.SLACK_TARGET_CHANNEL_ID
        self.my_user_id = settings.SLACK_USER_ID
        self.__reaction_notifications = {}  # 리액션 결과를 저장할 리스트

    def _get_recent_messages(self, limit=10) -> List[Dict]:
        """
        최근 메시지를 가져옵니다.
        """
        try:
            result = self.slack_client.conversations_history(channel=self.channel_id, limit=limit)
            return result["messages"]
        except SlackApiError as e:
            logger.error(f"Failed to fetch recent messages: {e.response['error']}")
            return []
        except Exception as e:
            logger.error(f"Failed to fetch recent messages: {e}")
            return []

    def _is_already_reacted(self, reactions, user_id) -> bool:
        """
        user_id가 이미 리액션을 달았는지 확인합니다.
        """
        return any(user_id in reaction["users"] for reaction in reactions)

    def react_to_message(self, message, emoji, reason):
        """
        이모지를 메시지에 추가합니다.
        """
        text: str = message["text"].replace("\n", "")[:50]
        logger.info(f"[REACT {emoji}] {reason} text='{text} (...)'")

        if settings.DRY_RUN:
            logger.debug("DRY_RUN enabled, skipping actual reaction.")
            return

        try:
            self.slack_client.reactions_add(channel=self.channel_id, name=emoji, timestamp=message["ts"])
        except SlackApiError as e:
            logger.warn(f"Error adding reaction: {e.response['error']}")

        # Store reaction notification.
        message_id = message["ts"]
        who = message["user"]
        self.__reaction_notifications.setdefault(
            message_id, {"emojis": [], "who": who, "text": text, "reason": reason}
        )
        self.__reaction_notifications[message_id]["emojis"].append(emoji)

    def send_report_to_DM_reaction_notifications(self):
        """
        1:1 DM으로 리액션 결과를 전송합니다.
        """
        if not settings.REPORT_RESULT_TO_DM or settings.DRY_RUN:
            return

        for info in self.__reaction_notifications.values():
            emojis = ", ".join([f":{e}:" for e in info["emojis"]])
            who = info["who"]
            reason = info["reason"]
            text = info["text"]
            message = f"from: <@{who}>\n{emojis} 를 {reason} 로 인해 달았습니다.\n`{text}`"

            # 봇을 통해 유저에게 메시지를 전송합니다.
            self.slack_bot_client.chat_postMessage(channel=settings.SLACK_USER_ID, text=message)

        self.__reaction_notifications.clear()

    def has_include_mention_in_message_text(self, message: Dict) -> bool:
        return '<@' in message['text']

    def _should_react(self, message: Dict, user_id):
        """
        반응해야 하는 메시지인지 확인합니다.
        """
        if not (reactions := message.get("reactions")):
            return

        if self._is_already_reacted(reactions, user_id):
            return

        # 인기있는 메시지 and 특정 유저에 대한 멘션이 없는 경우에만 반응합니다.
        #
        # 특정 유저들에게 보내는 메시지에 대한 반응을 막기 위해
        # 메시지 내에 멘션이 존재한다면 나에게 관련있는 메시지인지를 평가하는 위해 아래에서 처리합니다.
        for reaction in reactions:
            if reaction["count"] >= settings.NEED_REACTION_COUNT and not self.has_include_mention_in_message_text(
                message
            ):
                self.react_to_message(message, reaction["name"], reason="popular reaction count")

        # 채널 멘션에 반응합니다.
        channel_mention_triggers = ["<!here>", "<!channel>", "<!everyone>"]
        for trigger in channel_mention_triggers:
            if trigger in message["text"]:
                self.react_to_message(message, settings.EMOJI_MENTION_IN_CHANNEL_ALL_USERS, reason="Mention detected")
                break  # 한번만 반응하도록

        # 나에 대한 멘션에 반응합니다.
        if f"<@{user_id}>" in message["text"]:
            self.react_to_message(message, settings.EMOJI_MENTION_TO_ME, reason="Mention detected")

        # 내 팀에 대한 멘션에 반응합니다.
        if settings.SLACK_MYTEAM_ID in message["text"]:
            self.react_to_message(message, settings.EMOJI_MENTION_TO_MY_TEAM, reason="@MyTeam mention detected")

    def run(self):
        messages = self._get_recent_messages(settings.LAST_MESSAGES_LIMIT)

        for message in messages:
            self._should_react(message, self.my_user_id)

        self.send_report_to_DM_reaction_notifications()
