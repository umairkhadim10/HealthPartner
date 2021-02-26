import praw

from celery import shared_task
from .models import Tweets
from django_celery_beat.models import PeriodicTask,PeriodicTasks
from celery.schedules import crontab


def get_post_by_reddit_Api():
    # reddit = praw.Reddit(client_id='ISnOA13qK99q4A',
    #                      client_secret='cEKVwb65zJJoejN6YphDRamyHycdHA',
    #                      user_agent='my user agent')
    #
    # # to find the top most submission in the subreddit "GRE"
    # subreddit = reddit.subreddit('HEALTH')
    #
    # for submission in subreddit.top(limit=5):
    #     # displays the submission title
    #     tweets = Tweets(created_utc=submission.created_utc, description=submission.title)
    #     tweets.save()
    print('i ma kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')


