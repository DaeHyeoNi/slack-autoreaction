from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import logging_handler, settings
from emoji import Emoji

logger = logging_handler.logger


class SlackMonitor:
    def __init__(self, token, channel_id):
        self.slack_client = WebClient(token=token)
        self.channel_id = channel_id
        self.reaction_notifications = {}  # 리액션 결과를 저장할 리스트

    def _get_recent_messages(self, limit=10) -> List[Dict]:
        """
        최근 메시지를 가져옵니다.
        """
        result = self.slack_client.conversations_history(channel=self.channel_id, limit=limit)
        return result["messages"]

    def _is_already_reacted(self, reactions, user_id) -> bool:
        """
        user_id가 이미 리액션을 달았는지 확인합니다.
        """
        for reaction in reactions:
            if user_id in reaction["users"]:
                return True
        return False

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

        # 리액션 결과를 저장 (1:1 DM으로 결과를 전송할 때 사용)
        message_id = message["ts"]  # 슬랙 메시지의 타임스탬프를 고유 ID로 사용
        if message_id in self.reaction_notifications:
            # 이미 존재하는 메시지에 대해 추가적인 리액션 정보를 업데이트
            self.reaction_notifications[message_id]["emojis"].append(emoji)
        else:
            # 새로운 메시지에 대한 리액션 정보를 저장
            text = message.get("text", "")
            # 50자
            text = text.replace("\n", "")[:50]
            self.reaction_notifications[message_id] = {"emojis": [emoji], "text": text, "reason": reason}

    def send_reaction_notifications(self):
        """
        1:1 DM으로 리액션 결과를 전송합니다.
        """
        if not settings.REPORT_RESULT_TO_DM:
            return

        for _, info in self.reaction_notifications.items():
            emojis = ", ".join([f":{e}:" for e in info["emojis"]])
            reasons = ", ".join(info["reasons"])
            text = info["text"]
            message = f"{emojis} 를 {reasons} 로 인해 달았습니다.\n`{text}`"

            if settings.DRY_RUN:
                continue

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

        if "<!here>" in message["text"] or "<!channel>" in message["text"] or "<!everyone>" in message["text"]:
            self.react_to_message(message, Emoji.NEP, reason="Mention detected")

        if f"<@{user_id}>" in message["text"]:
            self.react_to_message(message, Emoji.NEP, reason="Mention detected")

        if "<!subteam^SUWJRKTCP|@backend>" in message["text"]:
            self.react_to_message(message, Emoji.EYES, reason="@backend detected")

    def run(self, user_id, last_message_limit=10):
        messages = self._get_recent_messages(last_message_limit)

        for message in messages:
            self._should_react(message, user_id)
