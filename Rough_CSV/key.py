from clear_state import good_tweets

keywords = ['lit', 'ratchet', 'adulting']

key_tweets = []

for keyword in keywords:
    for tweet in good_tweets:
        if keyword.lower() in tweet[4].lower():  
            key_tweets.append([keyword, tweet[0]])


#print(len(key_tweets))
#print(key_tweets)

matched_keyword = []

for tweet2 in good_tweets:
    for tweet in key_tweets:
        if tweet2[0] == tweet[1]: 
            matched_keyword.append([tweet + tweet2])
            


#print(matched_keyword)          



