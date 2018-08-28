
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token ="1012402072052957185-Txm1yLugHsMiTxTDMuaLUYY7kF7nLL"

access_token_secret = ""

consumer_key = "vdfRaONJbNQcWK5nqzUt34jIu"
consumer_secret = "EN9kfxsgJHxQ0gR2CGrno2DDdTzBxKXJHyltMWNCJWAViEheW9"



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'lit', 'ratchet', 'adulting'
    stream.filter(track=['lit', 'ratchet', 'adulting'])
