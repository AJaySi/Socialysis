#!/usr/bin/python
###########################################
#
# Below paramter = value is exposed to get more control on the tool.
# Do not mess with the left side values, right side should be something
# similar similar to the example values.
# It's WIP and more features will be added.
#
##########################################

# Please read README file in this directory on how to get below values.
consumer_key = mmUbrLagsNY38lds7PYEEPmrw
consumer_key_secret = N9eB7ZJQG8TKSWGRi3FDrBBmxBkWNWxbsuNU4svMvTv9SszhGM
access_token = 1082166100098375682-W4ka2RrEzEEbAVM3XqTi3pa0dUaoUO
access_token_secret = Fn22DbJaDBHxc0D9QEdRPJGmFH23ZjJiZOb44E1Rcg3QH

# Mention the number of tweets to fetch for a screen name, #tags, search queries.
num_of_tweets = 200

# Mention your criteria for trending twitter topics.
# most_likes takes maximum from all tweeets fetched, same as most_retweets.
# You can only mention 2 values as True OR False. Default is True.
most_likes = True
most_retweets = True 

# TBD : Fetch all tweets for a specified number of likes and retweets.
#likes = 1000
#retweets = 100

# TBD : Need to give controlling parameters for smart city. for -sm option.
# You can change the right side as permitted on twitter.
smartcity_search_keywords = 'pune smart city'

# TBD: need to mention the news channel twitter handles and hashtags. for -news option.

# TBD : List of Indian political parties twitter handles and hashtags. for -p option.