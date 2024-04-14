import asyncio
import json
from abc import ABCMeta, abstractmethod
from fastapi import WebSocket
from smskillsdk.models.api_async import SkillConversationMessage


def build_message(msg):
    msg_type_to_name = {
        SkillConversationMessage: "skillConversation",
        # ... register message names here
    }

    try:
        name = msg_type_to_name[type(msg)]
    except:
        raise KeyError("Trying to send unregistered message type")

    payload = msg.dict(exclude_none=True)
    return json.dumps({"name": name, "payload": payload}, default=lambda x: x.value)


class Connection(metaclass=ABCMeta):
    """Abstract interface to send messages over a connection."""

    @abstractmethod
    def send(self, msg):
        pass


class WsConnection(Connection):
    """Connection implementation for fastapi websocket (used by dev server)."""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    def send(self, msg):
        asyncio.run(self.websocket.send_text(build_message(msg)))
