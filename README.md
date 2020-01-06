This is a sample program to that shows hot to create a generic leaderboard using a ride share raiting example.

Assumptions:
* There are updates available in batch to be processed hourly
* There are millions of readers of the leaderboard every hour
* Assuming that the users of this rideshare system have an app that sends a trip raiting for every trip, and 
a thumbs up if the user liked it

### Goals:

1. A way to process the batched updates that makes sense for a scalable system.
2. Showing a way to calculate,query the leader board without a traditional database



### Tests:

1. Processing two taxi driver ratings makes the leader the first record when querying the leaderboard
2. [x] Given a file, it can be parsed in to useful data
3. Given a two parsable files, the leaderboard is updated to be consistent with the data from both files
 
### install
pip install -e . --user
