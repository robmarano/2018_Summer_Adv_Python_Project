from json_convert import tweets_data

states = [", AK", ", AL", ", AR", ", AZ", ", CA", ", CO", ", CT", ", DE", ", FL", ", GA", ", HI", ", IA", ", ID",
 ", IL", ", IN", ", KS", ", KY", ", LA", ", MA", ", MD", ", ME", ", MI", ", MN", ", MO", ", MS", ", MT", ", NC",
 ", ND", ", NE", ", NH", ", NJ", ", NM", ", NV", ", NY", ", OH", ", OK", ", OR", ", PA", ", RI", ", SC", ", SD",
 ", TN", ", TX", ", UT", ", VA", ", VT", ", WA", ", WI", ", WV", ", WY"]
good_tweets = []
locations = []
for tweet in tweets_data:
   # print(tweet.get('user', {}).get('location', {}))
    locations.append(tweet.get('user', {}).get('location', {}))
    for state in states:
        try:       
            if state in (tweet.get('user', {}).get('location', {})):
               # print('string contains a word from the word list: {}'.format(state))
                good_tweets.append(tweet)
            else:
                pass
        except:
            continue

print(len(good_tweets))
