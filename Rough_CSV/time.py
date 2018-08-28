from json_convert import tweets_data
import datetime

time = []
for tweet in tweets_data:
    time1 =datetime.datetime.strptime((tweet['created_at']), '%a %b %d %H:%M:%S +0000 %Y')
    time.append(time1)
    print(time1)
    print('Hour is {}, Time is {}'.format(time1.hour,time1.minute)) 
