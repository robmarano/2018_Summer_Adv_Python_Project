from replace_state import new_tweets
index_list = []

#for tweet in new_tweets
for index, value in enumerate(new_tweets, 1):
    index_list.append([index] + value)

print(index_list)
