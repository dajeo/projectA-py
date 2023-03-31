from dataclasses import dataclass
from typing import List

from fastapi import APIRouter, Depends
from redis import Redis
from starlette.websockets import WebSocket

from quark.database import get_redis
from quark.models import Customer, Performer
from quark.schemas import UserResponse
from quark.utils import get_current_ws_user

router = APIRouter()


@dataclass
class Connection:
    user: UserResponse
    websocket: WebSocket


def default_json(event_name: str, json: dict):
    return {
        "e": event_name,
        "o": json
    }


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Connection] = []

    async def connect(self, user: UserResponse, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(Connection(user, websocket))

    def disconnect(self, user: UserResponse):
        for connection in self.active_connections:
            if connection.user.id == user.id:
                self.active_connections.remove(connection)
                return

    async def __boardcast_to(self, type: int, customer: Customer, obj: dict):
        for connection in self.active_connections:
            if connection.user.type == type and connection.user.org == customer.user.org_id:
                await connection.websocket.send_json(obj)

    async def broadcast_to_customers(self, customer: Customer, obj: dict):
        await self.__boardcast_to(1, customer, obj)

    async def broadcast_to_performers(self, performer: Performer, obj: dict):
        await self.__boardcast_to(2, performer, obj)


manager = ConnectionManager()

@router.websocket("")
async def ws(websocket: WebSocket, user: UserResponse = Depends(get_current_ws_user), redis: Redis = Depends(get_redis)):
    await manager.connect(user, ws)

    pubsub = redis.pubsub(ignore_subscribe_messages=False)
    await pubsub.subscribe("ch1")

    while True:
        async for message in pubsub.listen():
            await websocket.send_json(message)

        await websocket.receive()
