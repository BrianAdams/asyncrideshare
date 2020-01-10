This is a sample program to that shows how to create a generic leaderboard using a ride share rating example.

Assumptions:
* There are updates available in batch to be processed hourly
* There are millions of readers of the leaderboard every hour
* Assuming that the users of this rideshare system have an app that sends a trip rating for every trip, and 
a thumbs up if the user liked it

### Goals:

1. A way to process the batched updates that makes sense for a scalable system.
2. Showing a way to calculate,query the leader board without a traditional database

### Contributing
This is not an ongoing project. Feel free to clone and use this if you find it useful. I'm not planning on accepting an contributions or changes.

### Using the web API
Browse API documentation
Swagger is used to document the API:
```
http://localhost:8080/docs
```

### Adding data
The system will monitor whatever path is pointed to by the `incomming_data_path` parameter.  It will attempt to parse any .json file it finds.

You can test easily by pointing to the `tests/incomming` folder and copying the  `tests/taxi_raitings.json` file in.

There is also a parameter `raw_data_path` that can point directly to a static raitings.json file which it will load on startup.

### Docker Setup
The fastest way to get started is to just run the environment in a docker container.
```
docker build -t process .

# You can run the web server (on windows replace $(pwd) with the path of the directory with the process project files)
docker run -it -v $(pwd)/tests:/data -p 8080:8000 process /usr/local/bin/process --raw_data_path=/data/taxi_raitings.json --incomming_data_path=/data/incomming server

# Point your browser to
http://localhost:8080/docs
```

### Non-Docker Setup
Setup the environment: This is using venv
```
>pip install -e .
>pip install -r requirements.txt
>pip install -r requirements/dev.txt
```

You can then try the program with
```
> process --raw_data_path tests/taxi_raitings.json lb
2020-01-10 10:01:21.618 | INFO     | process.repository:__init__:16 - Parsing file: tests/taxi_raitings.json
2020-01-10 10:01:21.620 | INFO     | process.repository:__init__:20 - Initalizing storage with 1 records.
{
    "highest_thumbs_up_ratio": {
        "1": {
            "driver_id": 123,
            "thumbs_up_ratio": 1.0,
            "thumbs_up_total": 1,
            "trip_time_minutes": 5,
            "trips": 1
        },
        "2": {
            "driver_id": 1234,
            "thumbs_up_ratio": 0.0,
            "thumbs_up_total": 0,
            "trip_time_minutes": 50,
            "trips": 1
        }
    },
    "most_trip_time": {
        "1": {
            "driver_id": 1234,
            "thumbs_up_ratio": 0.0,
            "thumbs_up_total": 0,
            "trip_time_minutes": 50,
            "trips": 1
        },
        "2": {
            "driver_id": 123,
            "thumbs_up_ratio": 1.0,
            "thumbs_up_total": 1,
            "trip_time_minutes": 5,
            "trips": 1
        }
    }
}

```

Or to run the webserver:
>  `SERVICE_PORT=8001 process --raw_data_path=tests/taxi_raitings.json --incomming_data_path=tests/incomming server`
Then point your your browser to http://localhost:8001/docs

### Pre-commit hooks
Run pre-commit install to install pre-commit into your git hooks. pre-commit will now run on every commit. Every time you clone this project running pre-commit install should always be the first thing you do.

If you want to manually run all pre-commit hooks on a repository, run pre-commit run --all-files. To run individual hooks use pre-commit run <hook_id>.

The first time pre-commit runs on a file it will automatically download, install, and run the hook. Note that running a hook for the first time may be slow. For example: If the machine does not have node installed, pre-commit will download and build a copy of node.


### Tests:

1. Processing two taxi driver ratings makes the leader the first record when querying the leaderboard
2. [x] Given a file, it can be parsed in to useful data
3. Given a two files, the leaderboard is updated to be consistent with the data from both files
 
### install
pip install -e . --user


### run tests
```
>pip install -e .
>pip install -r requirements.txt
>pip install -r requirements/dev.txt

>pytest
pytest
===================================================================== test session starts =====================================================================
platform linux -- Python 3.7.3, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /workspaces/asyncrideshare
plugins: asyncio-0.10.0
collected 2 items                                                                                                                                             

tests/test_leaderboard.py .                                                                                                                             [ 50%]
tests/test_stats_parser.py .                                                                                                                            [100%]

================================================================== 2 passed in 0.20 seconds ===================================================================
```
