#!/usr/bin/env python3

import datetime
from celery import Celery
from celery import group
import tweepy
import json
import tweepyconfig as config
import boto3

app = Celery('Celery_scheduler', broker='amqp://guest@localhost//', backend='amqp')


def tweepy_setup():

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)


def dynamo_setup():

    session = boto3.Session(profile_name='default')
    # Any clients created from this session will use credentials from the [default] section of ~/.aws/credentials.
    dev_s3_client = session.client('s3')
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    
    return dynamodb

def create_sample_tweets():

    tweet_id1 = {'tweet_id' :'1','tweet_id' : '2'}
    created_at1 = {'created_at' : '9 am','created_at' : '10 am'}
    location1 = {'location' : 'nebraska','location' : 'arkansas'}
    text1 = {'text' : 'it was lit','text' : 'thats ratchet'}

    tweet_id = json.dumps(tweet_id1)
    created_at = json.dumps(created_at1)
    location = json.dumps(location1)
    text = json.dumps(text1)

    sample_tweets = (tweet_id, created_at, location, text)
    
    return sample_tweets

@app.task
def makeit(dynamodb, *sample_tweets):
# Create the DynamoDB table.
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
#Unpacks tuple that was passed in as an argument from previous function
    tweet_id, created_at, location, text = sample_tweets

    add = table.put_item(
        Item =
        {
            'tweet_id': tweet_id,
            'created_at': created_at,
            'location': location,
            'text': text,
        }
    )
    print(table.item_count)

def set_celery_scheduler():

    app.conf.update(
        CELERYBEAT_SCHEDULE={
            'maketable-each-20-seconds': {
                'task': 'Celery_scheduler.makeit',
                'schedule': datetime.timedelta(seconds=20),
               # 'args': (2, )
            },
        },
    )



def main():
    
    tweepy_setup()
    dynamodb = dynamo_setup() 
    sample_tweets = create_sample_tweets()
    makeit(dynamodb, *sample_tweets)
    set_celery_scheduler()


main()
