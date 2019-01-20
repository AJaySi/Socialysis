# All Imports̥̥. Assuming python3 as requirement.
import tweepy
from textblob import TextBlob as tb
import pandas as pd     # To handle data
import numpy as np      # For number computing
from nltk.corpus import stopwords # For cleaning tweets
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
import itertools
import sys, os
import configparser
from io import StringIO

# Common utility function to get values from the config file 'tweelysis.conf'
def get_config(conf_type):

    # Dont have config sections as they get messed up over time.
    # Our conf file is user facing hence needs to inituitive enough.
    try:
        # Write a dummy header to satisfy configparser.
        conf = StringIO()
        conf.write('[dummy_twitter_section]\n')
        conf.write(open('tweelysis.conf').read())
        conf.seek(0, os.SEEK_SET)

        config = configparser.ConfigParser()
        config.read_file(conf)
    except Exception as e:
        print("Failed to login to twitter. Check 'twitter_credential.ini' file.", e)
        sys.exit(1)

    # Decide what needs to be returned from the config file.
    if ('tapi' in conf_type):
        consumer_key = config.get('dummy_twitter_section', 'consumer_key')
        consumer_key_secret = config.get('dummy_twitter_section', 'consumer_key_secret')
        access_token = config.get('dummy_twitter_section', 'access_token')
        access_token_secret = config.get('dummy_twitter_section', 'access_token_secret')

        # Return the keys.
        return (consumer_key, consumer_key_secret, access_token, access_token_secret)
    elif ('count' in conf_type):
        return(config.get('dummy_twitter_section', 'num_of_tweets'))
    
def get_twt_api():
    # Get the keys.
    #from tweelysis_conf import consumer_key, consumer_secret, access_token, access_token_secret
    consumer_key, consumer_key_secret, access_token, access_token_secret = get_config('tapi')

    # Create our tweepy API instance by passing auth instance into the API function of tweepy.
    # Try to get tweets with login credentials fetched from ini file.
    try:
        # Create twitter/tweepy OAuthHandler object
        auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
        # Pass/set access token and secret of twitter apis.
        auth.set_access_token(access_token, access_token_secret)
        t_api = tweepy.API(auth)
        # Internal methods of a single api object:
        # print(dir(api[0]))
        return(t_api)
    except:
        print("Twitter Authentication Error, Check your twitter APIs token.")
        sys.exit(1)

#Function to calculate tweet sentiment using textblob.
def get_sentiment(tweet):
    # Return a tuple of form (polarity, subjectivity ) where polarity is a float within 
    # the range [-1.0, 1.0] and subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective 
    # and 1.0 is very subjective.

    # Preprocess/Clean the tweets before sentiment analysis.
    analysis = tb(clean_tweets(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    elif analysis.sentiment.polarity < 0:
        return 'negative'


# Utility function to clean tweet text by html decoding, removing links, special characters 
# with regex statements. This is specifically for sentiment analysis.
def clean_tweets(tweet):
    """
    Utility function to do tweet data cleaning for sentiment analysis.
    Preprocessing: Remove special characters: str.replace('[^\w\s]','')
    Remove stopwords and stemming.
    Remove special characters, numbers, punctuations .str.replace("[^a-zA-Z#]", " ")
    Stemming is a rule-based process of stripping the 
    suffixes (“ing”, “ly”, “es”, “s” etc) from a word.
    """
    #TBD: use beautifulsoap for html decoding to normal text.
    # use HTMLparser to escape HTML characters from tweets.
    #html_parser = HTMLParser.HTMLParser()
    #tweet = html_parser.unescape(tweet)

    # Decode the data into UTF-8, for better sentiment analysis.
    #tweet = tweet.encode("ascii", 'ignore')
    # Remove @mention for sentiment analysis. As it adds no relevance to a sentence.
    tweet = re.sub(r'@[A-Za-z0-9]+','', tweet)
    # Strip out URL links as they are misleading for sentiment analysis.
    tweet = re.sub('https?://[A-Za-z0-9./]+','', tweet)
    # Strip '#' from the hashtags, leaving out the words. Consider only letters.
    tweet = re.sub("[^a-zA-Z]", " ", tweet)

    # Removal of Stop words, Human expressions(yey, haahahaha, etc), Punctuations.
    #stopword_set = set(stopwords.words("english"))
    #tweet = ''.join([w for w in tweet if w not in stopword_set])
    #print("STOP: {}".format(tweet))

    # Removing character repetitions. Ex: Hhappyyy to happy.
    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))

    tokens = word_tokenize(tweet)
    # remove all tokens that are not alphabetic
    tweet = ' '.join([word for word in tokens if word.isalpha()])

    # Stemming refers to the process of reducing each word to its root or base.
    # badly, worse, amazingly etc.
    porter = PorterStemmer()
    tweet = ' '.join([porter.stem(word) for word in tokens])

    # Return the tweet we consider cleaned for sentiment analysis.
    return(tweet)


def smartcity(smcity):
    print("Calling SM")
    pass