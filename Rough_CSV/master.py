import json

tweets_data_path = 'C:/Users/Kelly/Google Drive/stream2.txt'

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

states = [", AK", ", AL", ", AR", ", AZ", ", CA", ", CO", ", CT", ", DE", ", FL", ", GA", ", HI", ", IA", ", ID",
 ", IL", ", IN", ", KS", ", KY", ", LA", ", MA", ", MD", ", ME", ", MI", ", MN", ", MO", ", MS", ", MT", ", NC",
 ", ND", ", NE", ", NH", ", NJ", ", NM", ", NV", ", NY", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", ", SD",
 ", TN", ", TX", ", UT", ", VA", ", VT", ", WA", ", WI", ", WV", ", WY"]

good_tweets = []
locations = []
for tweet in zipped_list:
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


states1 = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID",
 "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC",
 "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD",
 "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]



words = ['lit', 'ratchet', 'adulting']

key_tweets = []

for word in words:
    for tweet in good_tweets:
        if word.lower() in tweet[4].lower():
            key_tweets.append([word, tweet[0]])

states_list = []
for state in states1:
    states_list.append([state])
#print(states_list)


#print(len(key_tweets))
#print(key_tweets)

matched_keyword = []

for tweet2 in good_tweets:
    for tweet in key_tweets:
        if tweet2[0] == tweet[1]:
            matched_keyword.append(tweet + tweet2)



#print(matched_keyword)


new_tweets = []

for tweet in matched_keyword:
    for state in states1:
        if state in tweet[5]:
            new_tweets.append(tweet + [state])

#print(new_tweets)

index_list = []

#for tweet in new_tweets
for index, value in enumerate(new_tweets, 1):
    index_list.append([index] + value)

#print(index_list)


import pandas as pd


final = []

for tweet in index_list:
    final.append([tweet[0]] + [tweet[8]] + [tweet[1]] + [tweet[4]])

#print(final)

df = pd.DataFrame(final)
df.to_csv('slang_big.csv', index=False, header=False)
