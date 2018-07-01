import tweepy
import json
import pprint

# Consumer keys and access tokens, used for OAuth, the consumer secret
# shouldn't be here as it should be kept secret
#WOEID for United States is woeid: 23424977

consumer_key = 'vdfRaONJbNQcWK5nqzUt34jIu'
consumer_secret = #can be found in project document
access_token = '1012402072052957185-Txm1yLugHsMiTxTDMuaLUYY7kF7nLL'
access_token_secret = 'TxxT2ZNiT8JY58bUcMlHAzmNjSZjrEunqLFRxkajEE7i7'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Sample method, used to update a status
# api.update_status('Hey everyone, testing the API!')

trends = api.trends_place(23424977)
pprint.pprint(trends)
