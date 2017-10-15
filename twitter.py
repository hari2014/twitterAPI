from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "789137681070501891-MfpJiKdI5AsBPh2fc9WpNEhsCNDw0dL"
access_token_secret = "6RomsMq11RQRFwQqotS8bc9R3HvwOVTPYwveYfRlqwBrR"
consumer_key = "OSkLrw7dObY6TWUiEQEeWYV2m"
consumer_secret = "e1ihsVsOhkE6ctyiNjGXef7L07bHLkOgc0rVTUc1CCXYlL0epv"


class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['python'])