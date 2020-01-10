import uvicorn
import os
from loguru import logger
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from decimal import Decimal
from process.controller import Controller

app = FastAPI()
app.version = 1.0


@app.get("/v1/leaderboard")
async def leaderboard():
    result = await controller.get_leaderboard()
    logger.info(f"result: {result}")
    return result


@app.get("/v1/ping")
async def ping():
    return "pong"


def start(_controller: Controller):
    global controller
    controller = _controller
    SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
