import praw
from textblob import TextBlob
import math

import time

def GetRedditTop():
    """
    Get Reddit top thread
    """
    from bs4 import BeautifulSoup
    import requests

    url = requests.get('https://redditmetrics.com/top')

    soup = BeautifulSoup(url.text, 'html.parser')

    aRet = []

    for subreddit in soup.find_all('a'):
        try:
            if '/r' in subreddit.string:
                aRet.append(subreddit.string[3:])
        except:
            TypeError
    return(aRet)

if(__name__=="__main__"):
    # Get the top lines
    aLines = GetRedditTop()

    if(len(aLines) > 0):
        reddit = praw.Reddit(client_id='uifJuvRl06uxTg', client_secret='Bf4eHDQhORvpJBw7syIvzat8gyA', user_agent='subSentiment')

        for line in aLines:
            subreddit = reddit.subreddit(line.strip())
            # write web agent to get converter for datetime to epoch on a daily basis for updates
            day_start = time.time()
            # 60 seconds * 60 minutes * 24 hours * 60 days = 2 months
            day_end = day_start - (60 * 60 * 24 * 60)
            query = 'timestamp:{}..{}'.format(day_start, day_end)

            sub_submissions = subreddit.search(query, sort='new')

            sub_sentiment = 0
            num_comments = 0

            for submission in sub_submissions:
                if not submission.stickied:
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                            blob = TextBlob(comment.body)

                            #adds comment sentiment to overall sentiment for subreddit
                            comment_sentiment = blob.sentiment.polarity
                            sub_sentiment += comment_sentiment
                            num_comments += 1

                            #prints comment and polarity
                            #print(str(comment.body.encode('utf-8')) + ': ' + str(blob.sentiment.polarity))

            print('/r/' + str(subreddit.display_name))
            try:
                print('Ratio: ' + str(math.floor(sub_sentiment/num_comments*100)) + '\n')
            except:
                print('No comment sentiment.' + '\n')
                ZeroDivisionError

    # add key:value subredditname:sentiment to dict
    # order dictionary by sentiment value
    # output dictionary key + ' sentiment: ' + sentiment value



