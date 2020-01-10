import uvicorn
import os
from loguru import logger
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from decimal import Decimal
from process.controller import Controller
from process.repository import Repository
from process.leaderboard import LeaderBoard
import asyncio

app = FastAPI()
app.version = 1.0
state = {}


@app.get("/v1/leaderboard")
async def leaderboard():
    result = await state["controller"].get_leaderboard()
    logger.info(f"result: {result}")
    return result


@app.get("/v1/ping")
async def ping():
    return "pong"


@app.on_event("startup")
def startup():
    logger.info("In startup")
    if "controller" not in state:
        repository = Repository(file=os.environ.get("raw_data_path"))
        leaderboard = LeaderBoard(repository)
        state["controller"] = Controller(leaderboard)
    file_watcher = asyncio.ensure_future(
        state["controller"].monitor_uploads(
            os.environ.get("incomming_data_path", "/data/incomming")
        )
    )


def start(_controller: Controller):
    logger.info("Starting up with the Controller")
    state["controller"] = _controller
    SERVICE_PORT = int(os.environ.get("SERVICE_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
