#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import requests
import time
import json
from datetime import datetime, timedelta
from striprtf.striprtf import rtf_to_text


# In[24]:


# alpha vantage api
f = open("/Users/anthonymarcovecchio/Desktop/AlphaVantageAPIKey.rtf", "r")
API_KEY = rtf_to_text(f.read())
f.close()

SYMBOL = 'TSLA'
FUNCTION = 'TIME_SERIES_DAILY'
OUTPUTSIZE = 'full'

url = f'https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&apikey={API_KEY}&outputsize={OUTPUTSIZE}'

response = requests.get(url).json()


# In[25]:


# examine response
print(json.dumps(response, indent=2))


# In[12]:


## Date adjustment helper functions

# Get non-weekend before/after dates (market closed on weekends)
def valid_price_dates(date_dt):
    
    # tweeted on a Friday - change day_after to Monday
    if date_dt.weekday() == 4:
        day_after_dt = date_dt + timedelta(3)
        day_prior_dt = date_dt - timedelta(1)
        
    # tweeted on a Saturday - change day_after to Monday
    elif date_dt.weekday() == 5 :
        day_after_dt = date_dt + timedelta(2)
        day_prior_dt = date_dt - timedelta(1)
        
    # tweeted on a Sunday - change day_prior to Friday
    elif date_dt.weekday() == 6:
        day_prior_dt = date_dt - timedelta(2)
        day_after_dt = date_dt + timedelta(1)
        
    # tweeted on a Monday - change day_prior to Friday
    elif date_dt.weekday() == 0:
        day_prior_dt = date_dt - timedelta(3)
        day_after_dt = date_dt + timedelta(1)
        
    else:
        day_prior_dt = date_dt - timedelta(1)
        day_after_dt = date_dt + timedelta(1)
    
    return day_prior_dt, day_after_dt

# Decrement day prior to next available weekday
def decrement_day_prior(day_prior_dt):
    
    day_prior_dt = day_prior_dt - timedelta(1)
    
    if day_prior_dt.weekday() == 6:
        day_prior_dt = day_prior_dt - timedelta(2)
    elif day_prior_dt.weekday() == 5:
        day_prior_dt = day_prior_dt - timedelta(1)
        
    return day_prior_dt

# Increment day after to next available weekday
def increment_day_after(day_after_dt):
    
    day_after_dt = day_after_dt + timedelta(1)
    
    if day_after_dt.weekday() == 5:
        day_after_dt = day_after_dt + timedelta(2)
    elif day_after_dt.weekday() == 6: 
        day_after_dt = day_after_dt + timedelta(1)
        
    return day_after_dt

# Return yyyy-mm-dd string from datetime
def dt_to_str(day_in_dt):
    
    return str(day_in_dt)[:10]


# In[ ]:


# Save all dates of Tesla share prices in csv
# Used for seperate exploratory/Google trends analysis
import csv  
header = ['Date', 'ClosePrice']
f = open('TeslaStockPrices.csv', 'w', encoding='UTF8')
writer = csv.writer(f)
writer.writerow(header)
for date in response['Time Series (Daily)']:
    ClosePrice = response['Time Series (Daily)'][date]['4. close']
    data = [date, ClosePrice]
    writer.writerow(data)
    print(f'{date}, {ClosePrice}')


# In[ ]:


## Append relative change in Tesla share price before/after a Tweet date

# Create dataframe
df = pd.read_csv('/Users/anthonymarcovecchio/Desktop/tweets.csv')

# Iterate through all Tweets --> Add % relative change in Tesla share price column
for index, row in df.iterrows():
    
    # convert date string in yyyy-mm-dd format to datetime
    tweet_date = row['Time']
    year = int(tweet_date[:4])
    month = int(tweet_date[5:7])
    day = int(tweet_date[8:10])
    date_dt = datetime(year, month, day, 0, 0, 0)

    # can't take open/close prices on day of tweet as may have been posted after market close
    day_prior_dt, day_after_dt = valid_price_dates(date_dt)
    
    # convert to yyyy-mm-dd format
    day_prior = dt_to_str(day_prior_dt)
    day_after = dt_to_str(day_after_dt)
    
    # handle market closure dates --> Call date adjustment functions as needed
    # close price of day prior to tweet
    try:
        tesla_prior = float(response['Time Series (Daily)'][day_prior]['4. close'])
    except:
        tesla_prior = None
        count = 0
        while tesla_prior is None:
            try:
                day_prior_dt = decrement_day_prior(day_prior_dt)
                day_prior = dt_to_str(day_prior_dt)
                tesla_prior = float(response['Time Series (Daily)'][day_prior]['4. close'])
            except:
                tesla_prior = None
                count += 1
                
                if count > 7:
                    tesla_prior = 0
                
    # close price of day after tweet
    try:
        tesla_after = float(response['Time Series (Daily)'][day_after]['4. close'])
    except:
        tesla_after = None
        count = 0
        while tesla_after is None:
            try:
                day_after_dt = increment_day_after(day_after_dt)
                day_after = dt_to_str(day_after_dt)
                tesla_after = float(response['Time Series (Daily)'][day_after]['4. close'])
                
            except:
                tesla_after = None
                count += 1
                
                if count > 7:
                    tesla_after = tesla_prior
                
    # calculate relative price changes (before/after tweet date using best available prices)
    tesla_change = ((tesla_after-tesla_prior)/tesla_prior)*100
        
    # set value of TeslaDelta
    df.at[index, 'Y'] = tesla_change
    df.at[index, 'Time'] = dt_to_str(date_dt)
    
    
    print(f'TweetDate: {tweet_date}, TeslaChange: {tesla_change:.4f}')
    
df.to_csv('/Users/anthonymarcovecchio/Desktop/TweetsTeslaPrices.csv', index=False)
