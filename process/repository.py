import json
import pathlib
from process.stats_parser import StatsParser
from loguru import logger

class Repository():
    """
    """
    def __init__(self, storage={}, file=None):
        self.storage=storage

        if file:
            parser = StatsParser()
            logger.info(f"Parsing file: {file}")
            reffile = pathlib.Path(file)
            self.storage=parser.parse_file(reffile)   

        logger.info(f"Initalizing storage with {len(self.storage)} records.")
    
    async def get_raw_stats(self):
        async for item in self.storage["ratings"]:
            yield item
            
    async def get_leaderboard_rollups(self):
        rollups = {}
        def calc(record):
            if record["driver_id"] not in rollups:
                rollups[record["driver_id"]] = {"trip_time_minutes":0}
            rollup = rollups[record["driver_id"]]
            rollup["trip_time_minutes"]+=record["trip_time_minutes"]


        [calc(record) for record in self.storage["ratings"]]

        return rollups