#!/usr/bin/env python3

import datetime
from celery import Celery
from celery import group
import tweepy
import json
import tweepyconfig as config
import boto3
import tweepy_pull as t

app = Celery('Celery_scheduler', broker='amqp://guest@localhost//', backend='amqp')



def dynamo_setup():
    '''Creates dynamodb resource to use for database table'''
    session = boto3.Session(profile_name='default')
    # Any clients created from this session will use credentials from the [default] section of ~/.aws/credentials.
    dev_s3_client = session.client('s3')
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    return dynamodb


def makeit(dynamodb):
    '''Creates dynamodb table'''
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

    return table

def fillit(table):

    filler_list = []
    filler = dict()

    #Creates a dictionary for selected components of each tweet, (tweet_id,
    #lang etc.) then combines all tweet dictionaries together in a list 
    for x in range(len(t.tweets)):
        filler = {}
        filler['tweet_id']= t.tweets[x]['id_str']
        filler['lang'] = t.tweets[x]['lang']
        filler['user_id'] = t.tweets[x]['user']['id']
        filler['location'] = t.tweets[x]['user']['location'] if \
        t.tweets[x]['user']['location'] else None
        filler['created_at'] = t.tweets[x]['created_at']
        filler['text'] = t.tweets[x]['text']
        filler_list.append(filler)

    #print(filler_list)
    #Adds all entries in list to dynamodb table at the same time
    with table.batch_writer() as batch:
        for item in filler_list:
            batch.put_item(Item=item)


def main():
    
    dynamodb = dynamo_setup() 
    table = makeit(dynamodb) 
    fillit(table)

main()
