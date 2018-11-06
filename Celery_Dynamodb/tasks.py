#!/usr/bin/env python3

import datetime
from celery import Celery
from celery import group
import tweepy
import json
import tweepyconfig as config
import boto3
from tweepy_pull import tweepy_setup, save_tweets

app = Celery('tasks.py', broker='redis://localhost:6379/0')

def dynamo_setup():
    '''Creates dynamodb resource to use for database table'''
    
    session = boto3.Session(profile_name='default')
    # Any clients created from this session will use credentials from the [default] section of ~/.aws/credentials.
    dev_s3_client = session.client('s3')
    # Get the service resource.

    dynamodb_resource = boto3.resource('dynamodb')
    dynamodb_client = boto3.client('dynamodb')

    client_resource = (dynamodb_client, dynamodb_resource)

    return client_resource

def makeit(*client_resource):
    '''Creates dynamodb table'''

    dynamodb_client, dynamodb_resource = client_resource

    table_exists = False
    try:
        table_description = dynamodb_client.describe_table(TableName='tweedata')
        table_exists = True

    except Exception as e:
        if "Requested resource not found: Table" in str(e):
                
            table = dynamodb_resource.create_table(
                TableName='tweedata',
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
            table.meta.client.get_waiter('table_exists').wait(TableName='tweedata')
            table_exists = True
        else:
            raise
    table = dynamodb_resource.Table('tweedata')

    return table

def fill_list(clean_tweets):
    '''Creates a dictionary for selected components of each tweet (tweet_id,
    lang etc.) then combined all tweet dictionaries together in a list'''

    filler_list = []
    filler = dict()

    for x in range(len(clean_tweets)):
        filler = {}
        filler['tweet_id']= clean_tweets[x]['id_str']
        filler['lang'] = clean_tweets[x]['lang']
        filler['user_id'] = clean_tweets[x]['user']['id']
        filler['location'] = clean_tweets[x]['user']['location'] if \
        clean_tweets[x]['user']['location'] else None
        filler['created_at'] = clean_tweets[x]['created_at']
        filler['text'] = clean_tweets[x]['text']
        filler_list.append(filler)

    return filler_list

def fillit(table, filler_list):
    '''Adds all tweets to Dynamodb at the same time in a batch'''

    with table.batch_writer() as batch:
        for item in filler_list:
            batch.put_item(Item=item)

@app.task
def celery_main():
    '''Main celery task, pulls tweets from twitter and saves in json format in
    tweepy_pull.py, creates dynamodb database if not existing, formats tweets
    appropriately for dynamodb and batch writes tweets to dynamodb'''

    cursor = tweepy_setup()
    save_tweets(cursor)
    clean_tweets = save_tweets(cursor)

    client_resource = dynamo_setup() 
    table = makeit(*client_resource) 

    fill_list(clean_tweets)
    filler_list = fill_list(clean_tweets) 
    fillit(table, filler_list) 


app.conf.update(
    CELERYBEAT_SCHEDULE={
        'populate-database-each-hour': {
            'task': 'tasks.celery_main',
            'schedule': datetime.timedelta(minutes=60),
           # 'args': (2, )
        },
    },
)

