# All Imports̥̥. Assuming python3 as requirement.
import tweepy
import re
import itertools
import argparse
import sys, os
from lib.main_dumb_lib import get_twt_api, get_sentiment

def get_tweets(tquery, count=10):
    # Login to twitter and get tweepy api object to get tweets.
    api = get_twt_api()
    tweets = []
    try:
        # Allow getting tweets by search query Or screen_name.
        tweets_list = api.search(q=tquery, count=count)
        # Iterate the publice_tweets array to check text sentiment of each tweet based on the polarity.
        for tweet in tweets_list:
            # Empty dict to store twitter params such as tweet:sentiment_analysis
            parsed_tweets = {}
            parsed_tweets['Tweet'] = tweet.text
            parsed_tweets['Sentiment'] = get_sentiment(tweet.text)

            if tweet.retweet_count > 0: 
                # if tweet has retweets, ensure that it is appended only once 
                if parsed_tweets not in tweets:
                    tweets.append(parsed_tweets)
            else: 
                tweets.append(parsed_tweets)
        # Return parsed tweets.
        print("The total number of tweets fetched: {}".format(len(tweets_list)))
        return(tweets)
    except tweepy.TweepError as e:
        print("Tweepy Error: Unable to fetch tweets.", e)