from utils.ws_connection import Connection
from smskillsdk.models.api_async import SessionStartMessage, SessionEndMessage


def session_start_handler(connection: Connection, msg: SessionStartMessage):
    """
    Session start handler

    Message sent to the skill at the start of the session, can be useful
    to do processing or caching on a per-session basis.
    """

    print("Session start handler got:", msg)


def session_end_handler(connection: Connection, msg: SessionEndMessage):
    """
    Session end handler

    Message sent to the skill at the end of the session, can be useful
    to clean up session resources or do end-of-session processing.
    """

    print("Session end handler got:", msg)
