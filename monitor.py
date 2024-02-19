from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import logging_handler, settings
from emoji import Emoji

logger = logging_handler.logger


class SlackMonitor:
    def __init__(self, token, channel_id):
        self.client = WebClient(token=token)
        self.channel_id = channel_id

    def _get_recent_messages(self, limit=10) -> List[Dict]:
        result = self.client.conversations_history(channel=self.channel_id, limit=limit)
        return result["messages"]

    def _is_already_reacted(self, reactions, user_id):
        for reaction in reactions:
            if user_id in reaction["users"]:
                return True
        return False

    def scanning_emoji_action(self, user_id, last_message_limit=10):
        logger.info(f"fetching recent messages")
        messages = self._get_recent_messages(last_message_limit)

        for message in messages:
            reactions = message.get("reactions")

            # 이미 반응한 메세지는 스킵
            if reactions and self._is_already_reacted(message["reactions"], user_id):
                continue

            # `NEED_REACTION_COUNT` 이상으로 반응이 일어난 이모지에 같은 이모지로 반응
            if reactions and message["reactions"]:
                for reaction in message["reactions"]:
                    if reaction["count"] >= settings.NEED_REACTION_COUNT:
                        self.react_to_message(message, reaction["name"], reason="popular reaction count")

            # '@here', '@channel', '@everyone' 와 같은 채널 멘션이 포함된 메세지에 "넵" 반응
            if "<!here>" in message["text"] or "<!channel>" in message["text"] or "<!everyone>" in message["text"]:
                self.react_to_message(message, Emoji.NEP, reason="Mention detected")

            # @user_id 멘션된 메세지에 "넵" 반응
            if f"<@{user_id}>" in message["text"]:
                self.react_to_message(message, Emoji.NEP, reason="Mention detected")

            # @backend 를 포함하는 메세지에 "눈" 반응
            if "<!subteam^SUWJRKTCP|@backend>" in message["text"]:
                self.react_to_message(message, Emoji.EYES, reason="@backend detected")

    def react_to_message(self, message, emoji, reason):
        try:
            text: str = message["text"].replace("\n", "")[:50]
            logger.info(f"[REACT {emoji}] {reason} text='{text}' (...)")

            if settings.DRY_RUN:
                return

            self.client.reactions_add(channel=self.channel_id, name=emoji, timestamp=message["ts"])
        except SlackApiError as e:
            logger.warn(f"Error adding reaction: {e.response['error']}")
