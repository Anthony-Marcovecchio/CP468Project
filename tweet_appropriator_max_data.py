import configparser
from tkinter import E
import tweepy
import pandas as pd
import numpy as np
import csv
import time
import datetime
from datetime import timedelta

#making sure not to overwrite tweets.csv accidentally
print("Running this script will erase all values currently in tweets.csv back it up now if you need those records.")
overwrite="y"
#overwrite=input("Do you wish to overwrite tweets.csv?  Y/N:     ")
if(overwrite=='y' or overwrite=='Y'):
    f=open("tweets_max_data_extension.csv",'w')
    fv=open("tweets2.csv","w")
    tv=open("IDs.txt","w")
    f.truncate
    
else:
    exit()
#make sure request timer is up
#time.sleep(930)

# read config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

#indicate when waiting for rate limits
api.wait_on_rate_limit=True
api.wait_on_rate_limit_notify=True


#create writer
writer2=csv.writer(fv)
#create dataframe
data=[]
columns = ['ID', 'Thread ID', 'ID of Tweet Replied to', 'User Replied to','Tweet Replied to', 'Tweet','Likes', 'Retweets','Replies', 'Ratio', 'Time','Entities']
df = pd.DataFrame(data, columns=columns)
rf=pd.read_csv('ids2.csv')
df.to_csv('tweets_max_data_extension.csv')

#df.to_csv('tweets.csv')
id_array=rf['id'].tolist()

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAOb%2BegEAAAAAjSdCMfIel0ohleowNshsRIgCpAc%3DG0ZHYgwQvID6mGPNLs6zsD7DYrT3gi48nQxeNqPdVYudKIwadf",wait_on_rate_limit=True)

def tweet_to_data(tweet,c):
    #run_count=1
    #r=0
    if tweet.user.screen_name==screen_name:
        reply_count=reply_array[c]
        reply_to=reply_to_array[c]
        thread_id=thread_id_array[c]
        if(reply_count==0):
            ratio=None
        else:
            ratio=tweet.favorite_count/reply_count
        row=[tweet.id, thread_id, tweet.in_reply_to_status_id , tweet.in_reply_to_screen_name, reply_to, tweet.text,  tweet.favorite_count, tweet.retweet_count, reply_count, ratio, tweet.created_at,tweet.entities   ]
        data.append(row)
        #writer2.writerows(row)
        #fv.write(",".join(row))
        df = pd.DataFrame(data, columns=columns)
        df.to_csv('tweets_max_data_extension.csv')
        #print("Run ", run_count, " complete.    ",datetime.datetime.now())
        #run_count+=1
        #r+=1
        #time.sleep(3.7)

screen_name="elonmusk"
last_id="588076749562318849" #last tweet we want to get
data=[]
reply_array=[]
reply_to_array=[]
tweets=[]
thread_id_array=[]
c=0
nrr=0#not retweet or reply (valid tweets)
client.wait_on_rate_limit=True
start_time=datetime.datetime.now()
for id in id_array:
    if id==1500030191837589510:
        exit()
    run_start_time=datetime.datetime.now()
    t=api.get_status(id)
    if  t.user.screen_name==screen_name:
        tweets.append(t)
        client_result = client.get_tweet(id, tweet_fields=["public_metrics"])
        tweet2 = client_result.data
        reply_count=tweet2.public_metrics["reply_count"]
        reply_array.append(reply_count)
        if t.in_reply_to_status_id is None:
            thread_id_array.append(t.id)
            reply_to_array.append(None)
        else:
            try:
                while current.in_reply_to_status_id is not None:
                    current=api.get_status(current.in_reply_to_status_id)
                thread_id=current.id #id of first tweet in thread
                thread_id_array.append(thread_id)
                reply_to_array.append(api.get_status(t.in_reply_to_status_id).text)

            except Exception:
                thread_id=1548165934296076288
                thread_id_array.append(thread_id)
                reply_to_array.append("A tweet in the thread was deleted.")
                pass


            current=t
            #while current.in_reply_to_status_id is not None:
            #    current=api.get_status(current.in_reply_to_status_id)
            #thread_id=current.id #id of first tweet in thread
            #thread_id_array.append(thread_id)
            #reply_to_array.append(api.get_status(t.in_reply_to_status_id).text)
        nrr+=1
    tweet_to_data(t,c)
    percentage=(c/len(id_array))*100
    percentage=round(percentage,2)
    current_time=datetime.datetime.now()
    time_elapsed=current_time-start_time
    if c>0:
        speed=c/(time_elapsed.total_seconds())
        if speed>0: 
            pred=(len(id_array)-c)/speed
            time_left=timedelta(seconds=len(id_array)/speed)
    else: 
        speed="N/A"
        time_left="N/A"
    
    print("Tweet ", str(c+1), "retrieved from ID.  | ",str(nrr), " valid tweets.  |  ", str(current_time),"  |   ",str(percentage), "%", "  |  Time elapsed: ",str(time_elapsed), "  |  Speed: ",str(speed), "  |  Estimated time left: ",str(time_left))
    c+=1


#df.to_csv('tweets.csv',mode='a',header=False)

#tweets = api.user_timeline(screen_name=screen_name,max_id=1438928760846290948,include_rts=False, exclude_replies=True)
#max_id="1546980241494745100"


f.close
fv.close

