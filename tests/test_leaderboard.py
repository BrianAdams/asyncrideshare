import json
import pathlib
import decimal
import asyncio
import pytest

from process.leaderboard import LeaderBoard
from process.stats_parser import StatsParser
from process.repository import Repository

@pytest.mark.asyncio
async def test_leaderboard_generates_stats(request):
    ''' This is a real test that is reprentative of the type of tests needed '''
    path = pathlib.Path(request.node.fspath)
    reffile = path.with_name('taxi_raitings.json')

    parser = StatsParser()
    repository = Repository(parser.parse_file(reffile))

    leaderboard = LeaderBoard(repository)
    result = await leaderboard.calculate_leaders()
    assert result["stats"]["most_trip_time"]["1"]["driver_id"] == 1234
    assert result["stats"]["most_trip_time"]["1"]["trip_time_minutes"] == 50
 