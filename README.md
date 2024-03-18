# Analysis of Elon Musk’s Twitter Presence and Tesla’s Stock Prices

###### Description
This project was completed as coursework for CP468 - Artificial Intelligence at Wilfrid Laurier University during the Spring 2022 term. Elon Musk has at times had a strong short-term influence on the price of Tesla shares due to a single Tweet. On more than several occasions, a Musk Tweet has caused the price of Tesla to change by around 10% in the positive or negative direction (https://www.bloomberg.com/news/articles/2021-11-09/seven-elon-musk-tweets-that-sent-tesla-shares-on-a-wild-ride). Thus, this project aimed to explore these trends and develop a model of the phenomena.

###### Objective
All models considered the number of a Tweet's likes, retweets, replies, as well as the ratio of likes to replies as predictors of the dependent variable of relative change in Tesla share price (closing price before/after Tweet date). In total four models were trained: (1) linear regression considering all Elon Musk Tweets starting Jan 1, 2015, (2) linear regression model considering only Tweets with > 100K likes starting Jan 1, 2015; (3) logistic regression with the relative change in price converted to a binary categorical variable (change in 'pos' or 'neg' direction); and (4) logistic regression following the same approach as #3, but only considering Tweets with > 100K likes.

###### Dataset
- Used Twitter API to pull Elon Musk Tweets
- Used AlphaVantage Stock API to pull Tesla stock data

###### Results
Linear regression - All Musk Tweets starting 2015:
  - MSE of 13.37, coefficeint of determination of 0.03
 
Linear regression - Musk Tweets with > 100K likes:
  - MSE of 5.23, coefficeint of determination of 0.46
  
Logistic regression - All Musk Tweets starting 2015:
  - Accuracy score of 71%
  
Logistic regression - Tweets with > 100K likes:
  - Accuracy score of 94%

###### Conclusion
- Reducing the dataset to Tweets with > 100K likes improved performance for both the linear regression and logistic regression models
- This can be interpreted as reducing the variance in training data
- Caveat of using Tweets > 100K likes is that reduced the sample size to 81 as opposed to the original 486 with all Tweets
- Logistic regression appeared to perform better than linear, which makes sense conceptually as magnitude shifts in stock prices are difficult to predict

###### About Developers
- Anthony Marcovecchio, BSc Computer Science and Psychology student at Wilfrid Laurier University
- Jules Mbende Bong, BSc Computer Science and Physics student at Wilfrid Laurier University

###### License to Use Code
Code may be used/modified at the discretion of those interested. Please note that model development was not intended to inform trading of Tesla securities. It is against the recommendation of the developers to use the model results to inform any decision to trade Tesla shares. Further statistical testing and validation are required to understand the risk of the existing model. 
