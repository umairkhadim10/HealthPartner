import os

from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthPartner.settings')

app = Celery('HealthPartner')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, get_post_by_reddit_Api.s("hello"), name='add every 10')


# Load task modules from all registered Django app configs.
# @app.on_after_finalize
# app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task()
def get_post_by_reddit_Api(arg):
    # reddit = praw.Reddit(client_id='ISnOA13qK99q4A',
    #                      client_secret='cEKVwb65zJJoejN6YphDRamyHycdHA',
    #                      user_agent='my user agent')
    #
    # # to find the top most submission in the subreddit "GRE"
    # subreddit = reddit.subreddit('HEALTH')
    #
    # for submission in subreddit.top(limit=5):
    #     # displays the submission title
    #     tweets = Tweets(user_name='hameeed', description=submission.title)
    #     tweets.save()
    print('i   kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
