#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
########################################################################

# Import required functionalities.
import argparse
import sys, os
import configparser
from io import StringIO
from lib.search_tweets import get_tweets
from lib.screen_name_tweets import get_screen_tweets

# Main function to parse the command line options and then
# call appripritate functions or exit with help message.
def parse_arguments():
    """
    Parse the command line argument and do as commanded. 
    Parameters: 
    Run with -h option to list all the paramters to control the test tool. 
    Returns: 
    N/A 
    """
    parser=argparse.ArgumentParser(
        # All are optional, default is to do nothing/lazy.
        usage='%(prog)s [-sm] OR [-md] OR [-sn]',
        formatter_class=argparse.RawTextHelpFormatter,
        #formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Command line tool to do twitter analysis.',
        epilog="Use %(prog)s as per examples above. Also, see the 'twelysis.conf' for controllig analysis."
    )
    # Define the type of rest method.
    parser.add_argument(
        # Not giving --smartcity, in lieu of lesser typing.
        "-sm",
        # I need this for logic, but removing below limitation will also remove one more 
        # paramters. hmmm, usuability is inversely proportional to number of steps/arguments.
        action='store_true',
        default='pune',
        required=False,
        # TBD: worldview: Good to know world's view on smart cities in india with non indian tweets.
        # Only consider indian cities being developed or talked about as smart cities.
        #choices=['Pune', 'Mumbai', 'Delhi', 'Bangalore', 'worldview'],
        help="Shows only 'Pune Smart city' tweets analysis.\n\
        To Be Done(TBDs) are Mumbai, Delhi, Bangalore, worldview.\n\
        1. Run As:  %(prog)s -sm\n\
        2. TBD: Run As: %(prog)s -sm give_any_smart_city_name\n"
    )
    # This option takes a valid twitter screen names and fetches tweets for a specified range.
    parser.add_argument(
        "-sn",
        metavar='',
        # Do an analysis of all news channel twitter handle. Default: India.
        default='NarendraModi',
        help="TBD: Do an analysis of all tweets for given twitter screen name.\n\
        Use this option as: %(prog)s -sn give_twitter_screen_name\n\
        Example: %(prog)s -sn NarendraModi\n"
    )
    # 
    parser.add_argument(
        "-ht",
        help="TBD: Analyse tweets of specified hasttags.\n\
        Use this option as: %(prog)s -ht #dontknow"
    )
    # Can we generate a summary of all the news around a screename, twitter topic.
    parser.add_argument(
        "-news",
        metavar='',
        # Do an analysis of all news channel twitter handle. Default: India.
        default='indian',
        help="TBD: Do an analysis of all tweets from Indian newspaper twitter handles.\n\
        Use this option as: %(prog)s -news"
    )
    # Analyze tweets from indian political parties. Elections2019/Winter is coming.
    # One should be able to specify a single party twitter account to analyze and
    # also political figures/screen_name.
    parser.add_argument(
        "-p",
        metavar='',
        # Do an analysis of all news channel twitter handle. Default: India.
        default='indian',
        help="TBD: Do an analysis of all tweets from Indian political parties twitter handles.\n\
        Use this option as: %(prog)s -p"
    )
    # Option to list/analyse most trending tweets. The problem is defining 'trending'.
    parser.add_argument(
        "-t",
        help="TBD: Analyse most trending. Use 'tweelysis.conf' file to define trending.\n\
        Use this option as: %(prog)s -t"
    )

    # If nothing is given, then you need help.
    if len(sys.argv)==1:
        print("Please read below and execute again. Also Check 'tweelysis.conf' in this directory.")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if (args.md):
        # Set the screen name as narendramodi for this selection/option.
        # Call the common get_screen_tweets.
        screen_name = 'NarendraModi'
        get_screen_tweets(screen_name)
    elif(args.sm):
        # For smart city, we are assuming certain twitter search queries, also defined in 
        # tweelysis.conf file. At the command prompt, we only ask for the city name.
        # TBD: for now, Default is pune.
        default_smrt_city = 'pune'
        smartcity(default_smrt_city)

# The init matrix function.
if __name__ == "__main__":
    """
    The main function to check the mode called in and give desired results in 
    form of tweets. The main job is make it simple to do tweets analysis generally 
    and specifically sentiment analysis.
    """
    # Lets parse the command line options first.
    parse_arguments()

#    tweets = get_tweets("Pune Smart city", count = 1000)
#    print(tweets)
#    # Picking positive tweets from tweets
#    # We create a pandas dataframe as follows:
#    data = pd.DataFrame(tweets, columns=['Tweets']) 
#    print(data.head(10))
#
#    ptweets = [tweet for tweet in tweets if tweet['Sentiment'] == 'positive'] 
#    # Picking negative tweets from tweets 
#    ntweets = [tweet for tweet in tweets if tweet['Sentiment'] == 'negative'] 
#    print("The total number of tweets processed and sentiment analysed: {}".format(len(tweets)))
#    
#    positive_correct = len(ptweets)
#    total_count = len(tweets)
#    negative_correct = len(ntweets)
#    # Percentage of positive tweets 
#    print("Positive Tweet percentage = {}%".format(positive_correct/total_count*100.0))
#    # Percentage of negative tweets
#    print("Negative Tweet percentage = {}%".format(negative_correct/total_count*100.0))
#    print("The total number of tweets processed and sentiment analysed: {}".format(total_count))