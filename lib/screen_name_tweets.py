# All Imports̥̥. Assuming python3 as requirement.
import tweepy
from textblob import TextBlob as tb
import pandas as pd     # To handle data
import numpy as np      # For number computing
import matplotlib.pyplot as plt   # For Graphing the data
import re
import itertools
import argparse
import sys, os
from lib.main_dumb_lib import get_twt_api, clean_tweets, get_sentiment, get_config
from tweets_analyzer import main
from visualization import wrdcloud

# Common function to ̥̥̥̥get/fetch tweets for a given twitter screen name.
def get_screen_tweets(scrn_name):
    """
    Utility function to fetch tweets for a given screen name parameter.
    Input: Provide a valid twitter screen name.
    Takes the number of tweeets to fetch and analyse also.
    """
    twt_cnt = get_config('count')
    try: 
        # setup_tweets will do exception handling.
        t_api = get_twt_api()
        #tweet_list = []
        # Now, that the twitter login and API is available, lets get screen_name tweets.
        #new_tweets = t_api.user_timeline(screen_name=scrn_name, count=twt_cnt)
        tweet_list = t_api.get_user(screen_name=scrn_name, count=twt_cnt)
        #tweet_list.extend(new_tweets)
        #oldest_tweet = tweet_list[-1].id - 1

        #while len(new_tweets) > 0:
        #    # The max_id param will be used subsequently to prevent duplicates
        #    new_tweets = t_api.user_timeline(screen_name=scrn_name, count=200, max_id=oldest_tweet)
        #    # save most recent tweets
        #    tweet_list.extend(new_tweets)
        #    # id is updated to oldest tweet - 1 to keep track
        #    oldest_tweet = tweet_list[-1].id - 1
        #    print ('{} tweets downloaded for {}'.format(len(tweet_list), scrn_name))

    except tweepy.TweepError as e:
        print("Tweepy Error: Unable to fetch tweets.", e)

    # Create a dataframe out of the tweets for easier manipulations et al.
    twt_df = pd.DataFrame(data=[tweet.text for tweet in tweet_list], columns=['{} Tweets'.format(scrn_name)])
    #print(twt_df.head(10))

    # tweepy returns interesting metadata, very useful for general analysis and trends.
    twt_df['Location'] = np.array([tweet.author.location for tweet in tweet_list])
    twt_df['WordCount']= np.array([len(tweet.text) for tweet in tweet_list])
    twt_df['Likes'] = np.array([tweet.favorite_count for tweet in tweet_list])
    twt_df["Retweets_count"] = np.array([tweet.retweet_count for tweet in tweet_list])
    twt_df['Posted_on'] = np.array([tweet.created_at for tweet in tweet_list])
    twt_df['Source'] = np.array([tweet.source for tweet in tweet_list])
    twt_df["Hashtags"] = np.array([tweet.entities.get('hashtags') for tweet in tweet_list])

    # Print/Display tweets with most likes and retweets.
    # TBD: We need to find out, who all/hashtags rweeted most.
    twt_df['Text'] = np.array([tweet.text for tweet in tweet_list])
    most_likes = np.max(twt_df['Likes'])
    mst_like_tweet = twt_df[twt_df.Likes == most_likes].index[0]
    print("\nFollowing Tweet received Most Likes: {}, Out of {} tweets fetched.\n {}"\
        .format(most_likes, len(tweet_list), twt_df['Text'][mst_like_tweet]))

    most_rt = np.max(twt_df['Retweets_count'])
    mst_rt_twt = twt_df[twt_df.Retweets_count == most_rt].index[0]
    print("\nFollowing tweet recevied {} Retweets, out of {} total tweets.\n{}"\
        .format(most_rt, len(tweet_list), twt_df['Text'][mst_rt_twt]))

    analysed_tweets = {}
    ptweets = []
    ntweets = []
    neutwt = []
    for tweet in tweet_list:
        # Empty dict to store twitter params such as tweet:sentiment_analysis
        analysed_tweets['Tweet'] = tweet.text
        analysed_tweets['Sentiment'] = get_sentiment(tweet.text)

        if (analysed_tweets['Sentiment'] == 'positive'):
            twt = clean_tweets(tweet.text)
            ptweets.append(twt)
        elif (analysed_tweets['Sentiment'] == 'negative'):
            twt = clean_tweets(tweet.text)
            ntweets.append(twt)
        elif (analysed_tweets['Sentiment'] == 'neutral'):
            neutwt.append(tweet.text)

    print("\nTotal number of followers for {} is {}".format(scrn_name, tweet_list[0].author.followers_count))
    # Print/display information on average length of all tweets fetched.     
    print("Average character length of {} tweets is {}".format(len(tweet_list), np.mean(twt_df['WordCount'])))
    print("\nThe total number of '{}' tweets fetched: {}".format(scrn_name, len(tweet_list)))
    # Percentage of positive tweets 
    print("Positive Tweet percentage = {}%".format(((len(ptweets))/(len(tweet_list)))*100.0))
    # Percentage of negative tweets
    print("Negative Tweet percentage = {}%".format(((len(ntweets))/(len(tweet_list)))*100.0))
    # Percentage of Neutral tweets.
    print("Neutral Tweet Percentage = {}%".format((len(neutwt)/(len(tweet_list))*100.0)))

    # Create a Word Cloud.
    wrdcloud(ptweets)

    # Check if activity keyword is set for tracking. 
    # Need to decide defaults for tweets_analyzer.py
    activity = False
    if (activity):
        # Call tweets_analyzer.py with the screen for added analysis.
        # Credits to : https://github.com/x0rz/tweets_analyzer
        main(scrn_name)