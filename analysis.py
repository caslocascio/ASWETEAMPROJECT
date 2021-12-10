import pandas as pd
from datetime import datetime
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import TextBlob


def count_reviews(df):
    """
    Count total reviews
    """
    return df['review'].count()


def check_aged_reviews(reviews, min_date):
    """
    Return the number of old reviews based on the threshold
    """
    # create a dataframe from a list of tuples
    df = pd.DataFrame(reviews, columns=['professor', 'class', 'date',
                                        'review', 'workload', 'agree',
                                        'disagree', 'funny'])
    # convert data types
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')
    # compare dates and count reviews that older than the min_date
    n_old_reviews = df[df['date'] <=
                       datetime.strptime(min_date, '%Y-%m-%d')].shape[0]
    # compare dates and count reviews that newer than the min_date
    n_new_reviews = df[df['date'] >
                       datetime.strptime(min_date, '%Y-%m-%d')].shape[0]

    return n_old_reviews, n_new_reviews


# calculate the sentiment score
def review_sentiment_analysis(df, pol_threshold=0.1, subj_threshold=0.5):
    """
    Score and lable review's sentiment
    """
    # text pre-processing
    # lower case
    df['review'] = df['review'].str.lower()
    # remove punctuation
    df['review'] = df['review'].str.replace('[{}]'.format(string.punctuation),
                                            '', regex=True)
    # remove stopwords
    stop = stopwords.words('english')
    df['review'] = df['review'].apply(lambda x: ' '.join(
                                      [word for word in str(x).split()
                                       if word not in (stop)]))
    # word stemming
    st = PorterStemmer()
    df['review'] = df['review'].apply(lambda x: ' '.
                                      join([st.stem(word) for word
                                            in str(x).split()]))
    # TextBlob returns polarity & subjectivity scores
    df['senti_score'] = df['review'].apply(lambda x: TextBlob(x).sentiment)
    df['polarity_score'] = df['senti_score'].apply(lambda x: x[0])
    df['subjectivity_score'] = df['senti_score'].apply(lambda x: x[1])
    # decide if the review is positive or negative based on the threshold
    df['senti_fl'] = 'neutral'
    df.loc[df['polarity_score'] < -pol_threshold, 'senti_fl'] = 'negative'
    df.loc[df['polarity_score'] > pol_threshold, 'senti_fl'] = 'positive'
    # decide if the review is objective or subjective based on the threshold
    df['sub_fl'] = 'objective'
    df.loc[df['subjectivity_score'] >
           subj_threshold, 'sub_fl'] = 'subjective'
    # return counts
    return df, df[df['senti_fl'] == 'positive'].shape[0],\
        df[df['senti_fl'] == 'neutral'].shape[0],\
        df[df['senti_fl'] == 'negative'].shape[0],\
        df[df['sub_fl'] == 'objective'].shape[0],\
        df[df['sub_fl'] == 'subjective'].shape[0]


def review_analysis(reviews):
    """
    Perform analysis on review contents
    """
    # create a dataframe from a list of tuples
    df = pd.DataFrame(reviews, columns=['professor', 'class', 'date',
                                        'review', 'workload', 'agree',
                                        'disagree', 'funny'])
    print(df.shape)
    print(df.tail())
    # convert data types
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')
    # count reviews
    n_reviews = count_reviews(df)
    # Judge if the reviews are too old
    n_old_reviews = check_aged_reviews(df, min_date='2007-01-01')
    # sentiment analysis
    df, n_pos, n_neu, n_neg, n_obj, n_sub = review_sentiment_analysis(df)

    return df, n_reviews, n_old_reviews, n_pos, n_neu, n_neg, n_obj, n_sub
