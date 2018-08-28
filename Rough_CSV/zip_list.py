
import json

tweets_data_path = 'C:/Users/Kelly/slang3.txt'

id = []
locations = []
lang = []
created_at = []
text = []
tweets_data = []
tweets_file = open(tweets_data_path, "rb")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
        locations.append(tweet.get('user', {}).get('location', {}))
        created_at.append(tweet.get('created_at', {}))
        text.append(tweet.get('text', {}))
        lang.append(tweet.get('lang', {}))
        id.append(tweet.get('id', {}))
    except:
        continue


zipped_tuples = zip(id, created_at, lang, locations, text)
#print(list(zipped_tuples))


zipped_list = []
for t in zipped_tuples:
    tt = list(t)
    zipped_list.append(tt)

