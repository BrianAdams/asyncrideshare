import json
import pathlib
import decimal

from process.stats_parser import StatsParser

def test_flat_files_can_be_parsed(request):
    ''' This is a real test that is reprentative of the type of tests needed '''
    path = pathlib.Path(request.node.fspath)
    reffile = path.with_name('taxi_raitings.json')

    parser = StatsParser()
    parseresult = parser.parse_file(reffile)
    
    #Ensure parser can parse int fields
    testResult = parseresult["ratings"][0]["driver_id"]
    assert testResult == 123
    
    #Ensure parser keeps precision in floats
    testResult = parseresult["ratings"][0]["trip_distance_km"]
    assert testResult == 0.3

    #Ensure parser gets all records
    testResult = len(parseresult["ratings"])
    assert testResult == 2