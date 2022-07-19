#!/usr/bin/env python
# coding: utf-8

# In[66]:


#for data
import pandas as pd
import numpy as np

#for plotting
import matplotlib.pyplot as plt
import seaborn as sns
 
#for statistical tests
import scipy
import statsmodels.formula.api as smf
import statsmodels.api as sm

#for machine learning
from sklearn import model_selection, preprocessing, feature_selection, ensemble, linear_model, metrics, decomposition


# In[67]:


df = pd.read_csv("/Users/anthonymarcovecchio/Desktop/TweetsTeslaPricesRelated.csv")
df.head()


# In[68]:


x = "Y"
fig, ax = plt.subplots(nrows=1, ncols=1,  sharex=False, sharey=False)
fig.suptitle(x, fontsize=20)
ax.title.set_text('TeslaChange Distribution')
variable = df[x].fillna(df[x].mean())
breaks = np.quantile(variable, q=np.linspace(0, 1, 11))
variable = variable[(variable > breaks[0]) & (variable < breaks[10]) ]
sns.distplot(variable, hist=True, kde=True, kde_kws={"shade": True}, ax=ax)
des = df[x].describe()
ax.axvline(des["25%"], ls='--')
ax.axvline(des["mean"], ls='--')
ax.axvline(des["75%"], ls='--')
ax.grid(True)
des = round(des, 2).apply(lambda x: str(x))
box = '\n'.join(("min: "+des["min"], "25%: "+des["25%"], "mean: "+des["mean"], "75%: "+des["75%"], "max: "+des["max"]))
ax.text(0.95, 0.95, box, transform=ax.transAxes, fontsize=10, va='top', ha="right", bbox=dict(boxstyle='round', facecolor='white', alpha=1))


# In[69]:


data = df[['Likes','Retweets','Replies','Ratio','Y']]
fig=plt.figure()
ax=fig.add_subplot()
n=100
ax.scatter(data["Retweets"],data["Y"],color="blue")
ax.set_xlabel("Retweets")
ax.set_ylabel("Y")
plt.show()


# In[70]:


data = df[['Likes','Retweets','Replies','Ratio','Y']]
fig=plt.figure()
ax=fig.add_subplot()
n=100
ax.scatter(data["Likes"],data["Y"],color="orange")
ax.set_xlabel("Likes")
ax.set_ylabel("Y")
plt.show()


# In[71]:


data = df[['Likes','Retweets','Replies','Ratio','Y']]
fig=plt.figure()
ax=fig.add_subplot()
n=100
ax.scatter(data["Replies"],data["Y"],color="red")
ax.set_xlabel("Replies")
ax.set_ylabel("Y")
plt.show()


# In[72]:


data = df[['Likes','Retweets','Replies','Ratio','Y']]
fig=plt.figure()
ax=fig.add_subplot()
n=100
ax.scatter(data["Ratio"],data["Y"],color="blue")
ax.set_xlabel("Ratio")
ax.set_ylabel("Y")
plt.show()


# In[73]:


# examine data, removing outliers
sorted_df = df.sort_values(by=['Y'], ascending=True)
sorted_df.head()


# In[96]:


## Model training
def train_regr_model(df):
    # Randomize row order
    df_random = df.sample(frac=1) 
    train_df = df_random[:(int((len(df)*0.8)))]
    test_df = df_random[(int((len(df)*0.8))):]

    regr_model = linear_model.LinearRegression()
    features = train_df[['Likes', 'Retweets','Replies','Ratio']]
    dependent = train_df['Y']
    regr_model.fit(features, dependent)
    return regr_model, test_df

## Model assessment
def assess_model(regr_model, test_df):
    pred_y = regr_model.predict(test_df[['Likes', 'Retweets','Replies','Ratio']])
    mse = metrics.mean_squared_error(test_df['Y'], pred_y)
    return mse

def display_data(pred_y, test_df, mse):
    print("First five predictions\n{}".format(pred_y[:5]))
    print("Real first five labels\n{}".format(test_df['Y'][:5]))
    print("Mean Squared Error {}".format(mse))
    return


# In[89]:


## Model Build --> All Tweets since 2015
regr_model, test_df = train_regr_model(df)
mse = assess_model(regr_model, test_df)
display_data(pred_y, test_df, mse)


# In[93]:


## Model Build --> All Tweets with >100K likes only (81 Tweets)
# Adjust dataframe
df_reduced = df[df['Likes'] > 100000]
regr_model, test_df = train_regr_model(df_reduced)
mse = assess_model(regr_model, test_df)
display_data(pred_y, test_df, mse)
