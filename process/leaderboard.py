import json
import logging
from process.repository import Repository


def _calc_most_strip_time(src,limit=10):
    i = 0
    result = {}
    for k, v in sorted(src.items(), key=lambda item: item[1]["trip_time_minutes"],reverse=True):
        i=i+1
        v["driver_id"]=k
        result[str(i)]=v 
        if i==limit:
            break
    return result

class LeaderBoard():
    """
    """
    def __init__(self, repository:Repository):
        self.repository = repository
    
    async def calculate_leaders(self):
        logging.error(self.repository)
        unsorted_leaderboard_rollups = await self.repository.get_leaderboard_rollups()
        leaders = {"stats" : {"most_trip_time":{}, "highest_thumbs_up_ratio":{} }}

        leaders["stats"]["most_trip_time"]=_calc_most_strip_time(unsorted_leaderboard_rollups)

        return leaders