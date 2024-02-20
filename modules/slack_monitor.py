from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import logging_handler, settings

logger = logging_handler.get_logger()


class SlackMonitor:
    def __init__(self, token, channel_id):
        self.slack_client = WebClient(token=token)
        self.channel_id = channel_id
        self.reaction_notifications = {}  # 리액션 결과를 저장할 리스트

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
            return

        try:
            self.slack_client.reactions_add(channel=self.channel_id, name=emoji, timestamp=message["ts"])
        except SlackApiError as e:
            logger.warn(f"Error adding reaction: {e.response['error']}")

        # Store reaction notification.
        message_id = message["ts"]
        self.reaction_notifications.setdefault(message_id, {"emojis": [], "text": text, "reason": reason})
        self.reaction_notifications[message_id]["emojis"].append(emoji)

    def send_reaction_notifications(self):
        """
        1:1 DM으로 리액션 결과를 전송합니다.
        """
        if not settings.REPORT_RESULT_TO_DM or settings.DRY_RUN:
            return

        for info in self.reaction_notifications.values():
            emojis = ", ".join([f":{e}:" for e in info["emojis"]])
            reason = ", ".join(info["reason"])
            text = info["text"]
            message = f"{emojis} 를 {reason} 로 인해 달았습니다.\n`{text}`"
            self.slack_client.chat_postMessage(channel=settings.SLACK_USER_ID, text=message)

        self.reaction_notifications.clear()

    def _should_react(self, message, user_id):
        """
        반응해야 하는 메시지인지 확인합니다.
        """
        if not (reactions := message.get("reactions")):
            return

        if self._is_already_reacted(reactions, user_id):
            return

        for reaction in reactions:
            if reaction["count"] >= settings.NEED_REACTION_COUNT:
                self.react_to_message(message, reaction["name"], reason="popular reaction count")

        channel_mention_triggers = ["<!here>", "<!channel>", "<!everyone>"]
        for trigger in channel_mention_triggers:
            if trigger in message["text"]:
                self.react_to_message(message, settings.EMOJI_MENTION_IN_CHANNEL_ALL_USERS, reason="Mention detected")
                break  # 한번만 반응하도록

        if f"<@{user_id}>" in message["text"]:
            self.react_to_message(message, settings.EMOJI_MENTION_TO_ME, reason="Mention detected")

        if settings.SLACK_MYTEAM_ID in message["text"]:
            self.react_to_message(message, settings.EMOJI_MENTION_TO_MY_TEAM, reason="@MyTeam mention detected")

    def run(self, user_id, last_message_limit=10):
        messages = self._get_recent_messages(last_message_limit)

        for message in messages:
            self._should_react(message, user_id)
