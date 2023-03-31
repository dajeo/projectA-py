from fastapi import FastAPI

import websocket


app = FastAPI()
app.include_router(websocket.router, "/ws")
