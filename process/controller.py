"""
Controller module handles the behavior of the service. Regardless or access method (HTTP Api, command-line)
the logic for executing the request is handled here.  As a controller all types should be native Python
as the access method is responsible for translating from Python types to that appopriate to the access method (example: Json, Txt)
"""

import os
import random
import asyncio
from loguru import logger
from process.leaderboard import LeaderBoard


class Controller:
    def __init__(self, leaderboard: LeaderBoard):
        self.leaderboard = leaderboard

    async def get_leaderboard(self):
        return await self.leaderboard.calculate_leaders()

    # Normally we would have a seperate process load the files in to the data store
    # But since we are doing all of this in memory, we will load the files in the
    # same process as the system generating the leaderboard.
    async def monitor_uploads(self, path):
        logger.info(f"Monitoring for incomming files every 5s: {path}")
        while True:
            for r, d, f in os.walk(path):
                for file in f:
                    if ".json" in file:
                        logger.info(f"Processing file {file}")
                        # There are several errror condition we would want to guard here
                        await self.leaderboard.repository.load_file(
                            os.path.join(r, file)
                        )
                        os.rename(
                            os.path.join(r, file),
                            os.path.join(r, file.replace("json", "processed")),
                        )
            await asyncio.sleep(5)
