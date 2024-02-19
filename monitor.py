import time
from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import settings
from emoji import Emoji


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

    def _need_empathy(self):
        return [Emoji.NEP, Emoji.CLAP]

    def scanning_emoji_action(self, user_id, last_message_limit=10):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] fetching recent messages")
        messages = self._get_recent_messages(last_message_limit)

        for message in messages:
            reactions = message.get("reactions")

            # if user already reacted to the message
            if reactions and self._is_already_reacted(message["reactions"], user_id):
                continue

            # if emoji count is greater than `NEED_REACTION_COUNT`
            if reactions and message["reactions"]:
                for reaction in message["reactions"]:
                    for emoji in self._need_empathy():
                        if reaction["name"] == emoji and reaction["count"] >= settings.NEED_REACTION_COUNT:
                            self.react_to_message(message, emoji, reason="popular reaction count")

            # Check if message contains '@here', '@channel', or '@everyone'
            if "<!here>" in message["text"] or "<!channel>" in message["text"] or "<!everyone>" in message["text"]:
                self.react_to_message(message, Emoji.NEP, reason="Mention detected")

            # Check if message contains @user_id
            if f"<@{user_id}>" in message["text"]:
                self.react_to_message(message, Emoji.NEP, reason="Mention detected")

            # Check if message contains backend
            if "<!subteam^SUWJRKTCP|@backend>" in message["text"]:
                self.react_to_message(message, Emoji.EYES, reason="@backend detected")

    def react_to_message(self, message, emoji, reason):
        try:
            text: str = message["text"].replace("\n", "")[:50]
            print(f"[REACT {emoji}] {reason} text='{text}'")

            if settings.DRY_RUN:
                return

            self.client.reactions_add(channel=self.channel_id, name=emoji, timestamp=message["ts"])
        except SlackApiError as e:
            print(f"Error adding reaction: {e.response['error']}")
