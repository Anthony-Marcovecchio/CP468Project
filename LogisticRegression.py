#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

#for machine learnings
from sklearn import model_selection, preprocessing, feature_selection, ensemble, linear_model, metrics, decomposition


# In[24]:


df = pd.read_csv("/Users/anthonymarcovecchio/Desktop/TweetsTeslaPricesRelated.csv")
df.head()


# In[ ]:


## Transform Y column to binary categorical variable (pos/neg)
for index, row in df.iterrows():
    
    data = float(df.at[index,'Y'])
    if data >= 0:
        df.at[index,'Y']='pos'
    else:
        df.at[index,'Y']='neg'


# In[60]:


## Model training
def log_regr_model(df):
    
    # Randomize row order
    df_random = df.sample(frac=1) 
    train_df = df_random[:(int((len(df)*0.8)))]
    test_df = df_random[(int((len(df)*0.8))):]
    
    features = train_df[['Likes', 'Retweets','Replies','Ratio']]
    dependent = train_df['Y']
    
    log_regr = linear_model.LogisticRegression()
    log_regr.fit(features, dependent)
    
    return log_regr, test_df

## Model assessment
def assess_model(log_regr, test_df):
    
    x_test = test_df[['Likes', 'Retweets','Replies','Ratio']]
    y_test = test_df[['Y']]                
    
    pred_y = log_regr.predict(x_test)
    score = log_regr.score(x_test, y_test)
    return score, pred_y

def display_data(pred_y, test_df, score):
    print("First five predictions\n{}".format(pred_y[:5]))
    print("Real first five labels\n{}".format(test_df['Y'][:5]))
    print("Model Score {:.4f}".format(score))
    return


# In[61]:


## Model Build --> All Tweets since 2015
log_regr, test_df = log_regr_model(df)
score, pred_y = assess_model(log_regr, test_df)
display_data(pred_y, test_df, score)


# In[64]:


## Confusion Matrix
cm = metrics.confusion_matrix(test_df[['Y']], pred_y)
plt.figure(figsize=(9,9))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15)
