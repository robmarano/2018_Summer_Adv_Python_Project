import json

tweets_data_path = '/home/vagrant/twitter_analysis/StateSlang/slang.txt'

id = []
locations = []
lang = []
created_at = []
text = []
tweets_data = []
tweets_file = open(tweets_data_path, "r")
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
    

#print(len(id))
#print(len(text))


zipped_tuples = zip(id, created_at, lang, locations, text)
#print(list(zipped_tuples))


zipped_list = []
for t in zipped_tuples:
    tt = list(t)    
    zipped_list.append(tt)

#print(zipped_list)

states = [", AK", ", AL", ", AR", ", AZ", ", CA", ", CO", ", CT", ", DE", ", FL", ", GA", ", HI", ", IA", ", ID",
 ", IL", ", IN", ", KS", ", KY", ", LA", ", MA", ", MD", ", ME", ", MI", ", MN", ", MO", ", MS", ", MT", ", NC",
 ", ND", ", NE", ", NH", ", NJ", ", NM", ", NV", ", NY", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", ", SD",
 ", TN", ", TX", ", UT", ", VA", ", VT", ", WA", ", WI", ", WV", ", WY"]
good_tweets = []
locations = []
#for tweet in zipped_list:
    #locations.append(tweet.get('user', {}).get('location', {}))
   # for state in states:
       # for n, state in enumerate(tweet):
           # try:
               # if state in tweet[3]:
                  #  tweet[3] = state
                   # print('string contains a word from the word list')
               # good_tweets.append(tweet)
               # else:
                #    pass
          #  except:
           #     continue

#print(list(zipped_list))

#[[update.  for tweet in zipped_list] for state in states]


#print(len(good_tweets))

from json_convert import tweets_data

states = [", AK", ", AL", ", AR", ", AZ", ", CA", ", CO", ", CT", ", DE", ", FL", ", GA", ", HI", ", IA", ", ID",
 ", IL", ", IN", ", KS", ", KY", ", LA", ", MA", ", MD", ", ME", ", MI", ", MN", ", MO", ", MS", ", MT", ", NC",
 ", ND", ", NE", ", NH", ", NJ", ", NM", ", NV", ", NY", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", ", SD",
 ", TN", ", TX", ", UT", ", VA", ", VT", ", WA", ", WI", ", WV", ", WY"]
good_tweets = []
locations = []
for tweet in zipped_list:
   # print(tweet.get('user', {}).get('location', {}))
    #locations.append(tweet.get('user', {}).get('location', {}))
    for state in states:
        try:
            if state in tweet[3]:
               # print('string contains a word from the word list: {}'.format(state))
                good_tweets.append(tweet)
            else:
                pass
        except:
            continue

print(len(good_tweets))
print(good_tweets) 

import datetime

hour = []
minute = []
time = []
for tweet in good_tweets:
    time1 = datetime.datetime.strptime((tweet[1]), '%a %b %d %H:%M:%S +0000 %Y')
    time.append(time1)
   # print(time1)
   # print('Hour is {}, Time is {}'.format(time1.hour,time1.minute))
    hour.append(time1.hour)
    minute.append(time1.minute)
print(hour)
print(minute)


keywords = ['adulting', 'lit', 'ratchet']

key_tweets = []

for tweet in good_tweets.lower():
   # print(tweet.get('user', {}).get('location', {}))
    #locations.append(tweet.get('user', {}).get('location', {}))
    for keyword in keywords:
            if keyword.lower() in tweet[4]:
               # print('string contains a word from the word list: {}'.format(state))
                key_tweets.append(keyword)
            else:
                print('what?')

print(len(key_tweets))

new_zip = zip(good_tweets,key_tweets,hour,minute)
#print(list(new_zip))

