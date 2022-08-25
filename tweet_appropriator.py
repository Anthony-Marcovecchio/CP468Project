import configparser
import tweepy
import pandas as pd
import numpy as np
import csv
import time
import datetime

#making sure not to overwrite tweets.csv accidentally
print("Running this script will erase all values currently in tweets.csv back it up now if you need those records.")
overwrite="y"
#overwrite=input("Do you wish to overwrite tweets.csv?  Y/N:     ")
if(overwrite=='y' or overwrite=='Y'):
    f=open("tweets.csv",'w')
    fv=open("tweets2.csv","w")
    tv=open("IDs.txt","w")
    #f.truncate
    
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
columns = ['ID', 'Tweet','Likes', 'Retweets','Replies', 'Ratio', 'Time']
df = pd.DataFrame(data, columns=columns)
rf=pd.read_csv('combined(2021-2022).csv')
rf1=pd.read_csv('tweets_by_year/2015-2020.csv')
rf2=pd.read_csv("tweets_by_year/2020.csv")
rf3=pd.read_csv('tweets_by_year/2019.csv')
rf4=pd.read_csv('tweets_by_year/2018.csv')
rf5=pd.read_csv('tweets_by_year/2017.csv')
rf6=pd.read_csv('tweets_by_year/2016.csv')
rf7=pd.read_csv('tweets_by_year/2015.csv')

#df.to_csv('tweets.csv')
id_array=rf['id'].tolist()
id_array=id_array+rf1['id'].tolist()
for r in id_array:
    tv.write(str(r)+',')
tv.close()
#id_array=id_array+rf2['id'].tolist()
#id_array=id_array+rf3['id'].tolist()
#id_array=id_array+rf4['id'].tolist()
#id_array=id_array+rf5['id'].tolist()
#id_array=id_array+rf6['id'].tolist()
#id_array=id_array+rf7['id'].tolist()

client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAOb%2BegEAAAAAjSdCMfIel0ohleowNshsRIgCpAc%3DG0ZHYgwQvID6mGPNLs6zsD7DYrT3gi48nQxeNqPdVYudKIwadf",wait_on_rate_limit=True)

def tweets_to_data(tweets,data):
    run_count=1
    r=0
    for tweet in tweets:
        if tweet.user.screen_name==screen_name:
            reply_count=reply_array[r]
            if(reply_count==0):
                ratio=None
            else:
                ratio=tweet.favorite_count/reply_count
            row=[tweet.id,tweet.text, tweet.favorite_count, tweet.retweet_count, reply_count, ratio, tweet.created_at   ]
            data.append(row)
            #writer2.writerows(row)
            #fv.write(",".join(row))
            df = pd.DataFrame(data, columns=columns)
            df.to_csv('tweets.csv')
        print("Run ", run_count, " complete.    ",datetime.datetime.now())
        run_count+=1
        r+=1
        #time.sleep(3.7)

screen_name="elonmusk"
last_id="588076749562318849" #last tweet we want to get
data=[]
reply_array=[]
tweets=[]
c=0
nrr=0#not retweet or reply (valid tweets)
client.wait_on_rate_limit=True
for id in id_array:
    t=api.get_status(id)
    if t.in_reply_to_status_id is None and t.user.screen_name==screen_name:
        tweets.append(t)
        client_result = client.get_tweet(id, tweet_fields=["public_metrics"])
        tweet2 = client_result.data
        reply_count=tweet2.public_metrics["reply_count"]
        reply_array.append(reply_count)
        nrr+=1
    percentage=(c/len(id_array))*100
    percentage=round(percentage,2)
    print("Tweet ", str(c), "retrieved from ID.     ",str(nrr), " valid tweets.      ", str(datetime.datetime.now()),"       ",str(percentage), "%")
    c+=1

tweets_to_data(tweets,data)
df.to_csv('tweets.csv',mode='a',header=False)

#tweets = api.user_timeline(screen_name=screen_name,max_id=1438928760846290948,include_rts=False, exclude_replies=True)
#max_id="1546980241494745100"


f.close
fv.close

