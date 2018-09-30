import tweepy
import json
import tweepyconfig as config
import oauth2


def tweepy_setup():
    '''Sets up tweepy API authorization using credentials from config file, kept
    separately. Uses tweepy cursor method with search method in order to
    paginate tweets to store for database, so same tweets will not be pulled
    again in repeated queries''' 

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    query = 'ratchet'

    cursor = tweepy.Cursor(api.search, q=query, count=100) 

    return cursor 


def save_tweets(cursor):
    '''Stores tweets in json format in order to prepare them for being placed
    in dynamodb database'''

    tweets = []
    item_count = 0

    for tweet in cursor.items():
        tweets.append(tweet._json)

        item_count +=1
        if item_count>=100:
            break

    json_tweets = json.dumps(tweets)

    #print(len(json_tweets))

    #print(type(json_tweets))

    #print(json_tweets)


def main():

    cursor = tweepy_setup()
    save_tweets(cursor)

main()
