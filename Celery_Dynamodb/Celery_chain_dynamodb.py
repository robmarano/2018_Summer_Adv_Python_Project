import datetime
from celery import Celery
from celery import group
import tweepy

#!/usr/bin/env python3
import boto3

consumer_key = 'vdfRaONJbNQcWK5nqzUt34jIu'
consumer_secret = ''
access_token = '1012402072052957185-Txm1yLugHsMiTxTDMuaLUYY7kF7nLL'
access_token_secret = 'TxxT2ZNiT8JY58bUcMlHAzmNjSZjrEunqLFRxkajEE7i7'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



app = Celery('Celery_chain_dynamodb', broker='amqp://guest@localhost//', backend='amqp')


session = boto3.Session(profile_name='default')
# Any clients created from this session will use credentials from the [default] section of ~/.aws/credentials.
# Above 2 lines are from the tutorial I would think it'd be wise to change the default location of the
# credentials file. Any Dummy could probably figure where it is if they compromise a system. S3 is amazon
# storage, and that's where the table gets stored.
dev_s3_client = session.client('s3')
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Create the DynamoDB table.

@app.task
def tweets(keyword):
#def tweets(keyword):
    searched_tweets = api.search(q=keyword, rpp=100, count=1000)
    print(searched_tweets)

    for tweet in searched_tweets:
        try:

            tweet_id = tweet['id_str']
            created_at = tweet['created_at']
            location = tweet['user']['location']
            text = tweet['text']

        except Exception:
            pass
@app.task
def makeit():
    table = dynamodb.create_table(
        TableName='tweedata1',
        KeySchema=[
            {
                'AttributeName': 'tweet_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tweet_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
# Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='tweedata1')
# Print out some data about the table.
    print(table.item_count)

#def add_rest():
    add = table.put_item(
        Item =
        {
            'tweet_id': { 'N' :  tweet_id},
            'created_at': {'S': created_at},
            'location': {'S': location},
            'text': {'S': text},
        }
    )
    print(table.item_count)



@app.task
def chain():
    return (tweets.si() | makeit.si() )



app.conf.update(
    CELERYBEAT_SCHEDULE={
        'pulltweets-each-15-seconds': {
            'task': 'Celery_chain_dynamodb.chain',
            'schedule': datetime.timedelta(seconds=20),
           # 'args': (2, )
        },
    },
)

#app.conf.update(
#    CELERYBEAT_SCHEDULE={
#        'pulltweets-each-15-seconds': {
#            'task': 'James.tweets',
#            'schedule': datetime.timedelta(seconds=20),
#           # 'args': (2, )
#        },
#    },
#)

#app.conf.update(
#    CELERYBEAT_SCHEDULE={
#        'maketable-each-20-seconds': {
#            'task': 'James.makeit',
#            'schedule': datetime.timedelta(seconds=20),
#           # 'args': (2, )
#        },
#    },
#)
