import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import read_json
import argparse
import string
import json
from datetime import datetime, timedelta
import json_reader
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import memcache
import operator
import collections
from operator import itemgetter
from collections import Counter
import os


access_token = "789137681070501891-MfpJiKdI5AsBPh2fc9WpNEhsCNDw0dL"
access_token_secret = "6RomsMq11RQRFwQqotS8bc9R3HvwOVTPYwveYfRlqwBrR"
consumer_key = "OSkLrw7dObY6TWUiEQEeWYV2m"
consumer_secret = "e1ihsVsOhkE6ctyiNjGXef7L07bHLkOgc0rVTUc1CCXYlL0epv"



count_all2 = Counter()
time_all = {}
start_time = datetime.now()

mc = memcache.Client(['127.0.0.1:11211'], debug=0)


def process_datetime(data):
    try:
        tweet = json.loads(data)

        tweet_time = datetime.strptime(tweet['created_at'][:20] + tweet['created_at'][26:], '%a %b %d %X %Y')

        return tweet_time
    except Exception as e:
        ii =1


def get_parser():
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')

    return parser


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            global start_time
            terms_cur = read_json.process_text(data)
            time_cur = process_datetime(data)
            term_time = {term: time_cur for term in terms_cur}
            time_all.update(term_time)

            count_all2.update(terms_cur)
            mc.set_multi(count_all2)
            terms = list(count_all2)

            for term in terms:
                if (datetime.utcnow() - time_all[term]) > timedelta(seconds=30):
                    count_all2[term] = count_all2[term] - 1

                if count_all2[term] < 0:
                    del count_all2[term]
                    mc.delete(term)


            if (datetime.now() - start_time) > timedelta(seconds=60):
                start_time = datetime.now()
                os.system('clear')
                with open('count.txt', 'w', encoding='utf-8') as f:
                    for k, l in sorted([(j, i) for i, j in count_all2.items()], reverse=True):
                        f.write(l + ' : ' + str(k) + '\n')
                        try:
                            print(l + ' : ' + str(k))
                        except:
                            continue

            return True
        except BaseException as e:
            pass
        return True

    def on_error(self, status):
        pass


if __name__ == '__main__':


    parser = get_parser()
    args = parser.parse_args()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    while True:
        try:
            twitter_stream = Stream(auth, MyListener(args.query))
            twitter_stream.filter(track=[args.query])
        except:
            pass



