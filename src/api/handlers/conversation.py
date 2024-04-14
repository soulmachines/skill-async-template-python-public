from utils.ws_connection import Connection
from smskillsdk.models.api_async import (
    UserConversationMessage,
    SkillConversationMessage,
)


def conversation_handler(connection: Connection, request: UserConversationMessage):
    """
    Conversation handler

    Runs when a conversation message from the user is sent to the skill.
    """

    print("Conversation handler got:", request)

    if request.variables and request.variables.get("kind", "") == "init":
        welcome_message = "Hi there"
        connection.send(SkillConversationMessage(text=welcome_message))
        return

    connection.send(SkillConversationMessage(text=f"Echo: {request.text}"))
