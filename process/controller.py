"""
Controller module handles the behavior of the service. Regardless or access method (HTTP Api, command-line)
the logic for executing the request is handled here.  As a controller all types should be native Python
as the access method is responsible for translating from Python types to that appopriate to the access method (example: Json, Txt)
"""

import os
import random
from loguru import logger
from process.leaderboard import LeaderBoard

class Controller():

    def __init__(self, leaderboard:LeaderBoard):
        self.leaderboard = leaderboard 

    async def get_leaderboard(self):
        return await self.leaderboard.calculate_leaders()

