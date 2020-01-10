import json
import pathlib
import asyncio
from process.stats_parser import StatsParser
from loguru import logger


class Repository:
    """
    """

    def __init__(self, storage=None, file=None):
        if not storage:
            storage = {"ratings": []}
        self.storage = storage

        asyncio.get_event_loop().run_until_complete(self.load_file(file))
        size = len(self.storage["ratings"])

        logger.info(f"Initalizing storage with {size} records.")

    async def load_file(self, file=None):
        if file:
            parser = StatsParser()
            logger.info(f"Parsing file: {file}")
            reffile = pathlib.Path(file)
            new_data = parser.parse_file(reffile)["ratings"]
            self.storage["ratings"] += new_data

    async def get_raw_stats(self):
        async for item in self.storage["ratings"]:
            yield item

    async def get_leaderboard_rollups(self):
        rollups = {}

        def calc(record):
            if record["driver_id"] not in rollups:
                rollups[record["driver_id"]] = {
                    "trip_time_minutes": 0,
                    "thumbs_up_ratio": 0,
                    "thumbs_up_total": 0,
                    "trips": 0,
                }

            rollup = rollups[record["driver_id"]]
            rollup["trip_time_minutes"] += record["trip_time_minutes"]
            if record["trip_thumbs_up"]:
                rollup["thumbs_up_total"] += 1
            rollup["trips"] += 1
            rollup["thumbs_up_ratio"] = rollup["thumbs_up_total"] / rollup["trips"]

        for record in self.storage["ratings"]:
            calc(record)

        return rollups
