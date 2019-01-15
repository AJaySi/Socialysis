# All Imports̥̥. Assuming python3 as requirement.
import matplotlib.pyplot as plt   # For Graphing the data
import seaborn as draw
import pandas as pd
import re
import sys, os
from wordcloud import WordCloud

# Functiont to check the polarity and subjectivity of each line.
# This will store the results in CSV for later processing.
def check_data_distribution():
    all_reviews, polarity_list, subjectivity_list=[],[],[]
    
    with open("training_sentiments.txt", "r") as f:
        # TBD : As files will have millions of record, 
        # consider readlines method, etc.
        for aline in f.read().split('\n'):
            # Preprocessing: Remove special characters: str.replace('[^\w\s]','')
            # Remove stopwords and stemming.
            # Remove special characters, numbers, punctuations .str.replace("[^a-zA-Z#]", " ")
            # Stemming is a rule-based process of stripping the 
            # suffixes (“ing”, “ly”, “es”, “s” etc) from a word.
            tb_object = tb(aline)
            polarity_list.append(tb_object.sentiment.polarity)
            subjectivity_list.append(tb_object.sentiment.subjectivity)
            all_reviews.append(aline)

    # Save the polarity and subjectivity in a CSV file with panda.
    polarity_df = pd.DataFrame(polarity_list, columns=["colummn"])
    polarity_df.to_csv('polarity_list.csv', index=False)

    subjectivity_df = pd.DataFrame(subjectivity_list, columns=["colummn"])
    subjectivity_df.to_csv('subjectivity_list.csv', index=False)

    # Plot the distribution graph of polarity and subjectivity for all line/reviews.
    show_distplot(polarity_list)
    #Subjectivity Distribution
    show_distplot(subjectivity_list)

    #Getting statistical summary of polarity & subjectivity
    print(stats.describe(polarity_list))
    print(stats.describe(subjectivity_list))

    cnt = 0
    for i in range(len(polarity_list)):
        if(cnt>5): break
        if(polarity_list[i]>.9 and cnt < 5):
            print("Highest Polarity: {} and sentence: {}".format(polarity_list[i], all_reviews[i]))
            cnt += 1
            # print("Highly objective/Factual: {} Sentence: {}".format(subjectivity_list[i], all_reviews[i]))

    #Lets check few highly negative reviews with very high Polarity(<-.9)
    c = 0
    for i in range(len(polarity_list)):
        if(c>5): break
        if(polarity_list[i] < -0.9 and c < 5) :
            print("Most negative sentences: {}".format(all_reviews[i]))
            c+=1

# Takes a list of polarities and subjectivity to plot graph.
def show_distplot(data_2_plot):
    # Plot the distribution graph of polarity and subjectivity for all line/reviews.
    draw.set(color_codes=True)
    print("The Polarity distribution Graph below:")
    draw.distplot(data_2_plot)
    plt.show()

# Common function to plot wordcloud of tweets fetched. 
# This helps in giving high level view of most words frequency/used.
# Accepts a list of preprocessed tweets.
def wrdcloud(tweets_list):
    # Create a Word Cloud.
    ptwt = ' '.join(str(twt) for twt in tweets_list)
    wordcloud = WordCloud(width=1600, height=800,max_font_size=200).generate(ptwt)
    plt.figure(figsize=(12,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()