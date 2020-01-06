import json

class StatsParser():
    """
    This is a class so that if we have really large files, we can encapsulate the state of the parser and introduce paging and similar patterns.
    """
    def __init__(self):
        pass
    
    def parse_file(self, src_file):
        with src_file.open() as fp:
            return json.load(fp)
