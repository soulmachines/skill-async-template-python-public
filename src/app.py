import argparse
import json
import nest_asyncio
import uvicorn
from http import HTTPStatus
from fastapi import (
    FastAPI,
    status,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    Request,
)
from smskillsdk.models.api_async import (
    UserConversationMessage,
    SessionStartMessage,
    SessionEndMessage,
)
from smskillsdk.models.api import InitRequest

from api.handlers.conversation import conversation_handler
from api.handlers.end_project import delete_endpoint_endproject_handler
from api.handlers.init import init_handler
from api.handlers.session import session_end_handler, session_start_handler
from utils.ws_connection import WsConnection

nest_asyncio.apply()
app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                if "name" not in message or "payload" not in message:
                    print("Expecting event body to contain 'name' and 'payload' fields")

                action = message["name"]
                action_map = {
                    "conversation": (conversation_handler, UserConversationMessage),
                    "sessionStart": (session_start_handler, SessionStartMessage),
                    "sessionEnd": (session_end_handler, SessionEndMessage),
                }

                if action in action_map:
                    handler, msg_type = action_map[action]
                    payload = message["payload"]
                    handler(WsConnection(websocket), msg_type(**payload))
                else:
                    print("Unrecognized message name")
            except Exception as error:
                print("Handling error encountered:", error)

    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/init", status_code=status.HTTP_202_ACCEPTED)
def init(request_data: InitRequest, request: Request):

    init_handler(request_data)
    response = make_response(status=HTTPStatus.ACCEPTED)

    status_code = response.get("statusCode", status.HTTP_500_INTERNAL_SERVER_ERROR)
    if status_code != status.HTTP_202_ACCEPTED:
        raise HTTPException(status_code, detail=response.get("body", ""))

    return json.loads(response.get("body", "{}"))


@app.delete("/delete/{id}", status_code=status.HTTP_202_ACCEPTED)
def endpoint_endproject(id: int, request: Request):

    delete_endpoint_endproject_handler(id)
    response = make_response(HTTPStatus.ACCEPTED)

    status_code = response.get("statusCode", status.HTTP_500_INTERNAL_SERVER_ERROR)
    if status_code != status.HTTP_202_ACCEPTED:
        raise HTTPException(status_code, detail=response.get("body", ""))

    return json.loads(response.get("body", "{}"))


RESPONSE_HEADERS = {"Content-Type": "application/json"}


# Helper functions
def make_response(status=HTTPStatus.OK, body="{}"):
    """Helper function to make a formatted response."""

    return {
        "headers": RESPONSE_HEADERS,
        "statusCode": status,
        "body": body,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0", help="default - 0.0.0.0")
    parser.add_argument("--port", type=int, default=5000, help="default - 5000")
    parser.add_argument(
        "--autoreload",
        action="store_true",
        default=False,
        help="enables the uvicorn server to autoreload when changes are detected (default - False)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="number of workers that should be created for the uvicorn server (default - 1)",
    )
    args = parser.parse_args()

    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.autoreload,
        workers=args.workers,
        loop="asyncio",
    )
