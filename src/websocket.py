import json
import random
from typing import Any

from websockets import connect

from .credentials import WEBSOCKET_URL
from .logger import Logger


async def connect_websocket(
    websocket_url: str, data: Any, logger: Logger | None = None
):
    async with connect(websocket_url) as websocket:
        # Convert JSON data to string
        json_string = json.dumps(data)

        # Send JSON string via WebSocket
        await websocket.send(json_string)
        if logger is not None:
            logger.info("Sent JSON data")
            logger.info(json_string)
        await websocket.close()


async def open_websocket(
    speaker_alias: str,
    message: str,
    logger: Logger | None = None,
):
    data_id = random.randrange(
        10000, 99999
    )  # give each packet "unique" id for debugging purposes

    data = {
        "request": "Speak",
        "id": f"{data_id}",
        "voice": f"{speaker_alias}",
        "message": f"{message}",
    }

    print(f"Sending Packet with ID {id}")

    await connect_websocket(WEBSOCKET_URL, data, logger)

    pass
