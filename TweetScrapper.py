import configparser
import tweepy
import pandas as pd
import csv
import time

#making sure not to overwrite tweets.csv accidentally
print("Running this script will erase all values currently in tweets.csv back it up now if you need those records.")
overwrite=input("Do you wish to overwrite tweets.csv?  Y/N:     ")
if(overwrite=='y' or overwrite=='Y'):
    f=open("tweets.csv",'w')
    f.truncate
    f.close
else:
    exit()
#make sure request timer is up
time.sleep(930)

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
wait_on_rate_limit=True
wait_on_rate_limit_notify=True

#create dataframe
data=[]
columns = ['ID', 'Tweet','Likes', 'Retweets','Replies', 'Ratio', 'Time']
df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets.csv')

def tweets_to_data(tweets,data):
    for tweet in tweets:
        if tweet.user.screen_name==screen_name:
            client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAOb%2BegEAAAAAjSdCMfIel0ohleowNshsRIgCpAc%3DG0ZHYgwQvID6mGPNLs6zsD7DYrT3gi48nQxeNqPdVYudKIwadf")
            client_result = client.get_tweet(tweet.id, tweet_fields=["public_metrics"])
            tweet2 = client_result.data
            reply_count=tweet2.public_metrics["reply_count"]
            if(reply_count==0):
                ratio=None
            else:
                ratio=tweet.favorite_count/reply_count
            row=[tweet.id,tweet.text, tweet.favorite_count, tweet.retweet_count, reply_count, ratio, tweet.created_at   ]
            data.append(row)

screen_name="elonmusk"
last_id="588076749562318849"

tweets = api.user_timeline(screen_name=screen_name,include_rts=False, exclude_replies=True,count=1)
#max_id="1546980241494745100"
data=[]
for tweet in tweets:
    current_id=tweet.id
    #tweets_to_data(tweets,data)
    #df = pd.DataFrame(data,columns=columns)
    #df.to_csv('tweets.csv',mode='a',header=False)
run_count=0


while current_id!=last_id: #until we get to the oldest tweet
    tweets = api.user_timeline(screen_name=screen_name, max_id=current_id,include_rts=False,exclude_replies=True, count=200)

    tweets_to_data(tweets,data)
    if run_count>0:
        data.pop(0)
    df = pd.DataFrame(data,columns=columns)
    df.to_csv('tweets.csv',mode='a',header=False)

    current_id=data[-1][0]
    run_count+=1
    time.sleep(930)
    

