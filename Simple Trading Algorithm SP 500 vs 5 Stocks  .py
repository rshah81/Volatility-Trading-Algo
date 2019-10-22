#!/usr/bin/env python
# coding: utf-8

# In[1]:


"Rishabh Shah"
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


# Part 1 - Data Preparation
# 1. Calculate returns on the prices for all assets (included the S&P 500).
# 2. Calculate returns in excess of the market return by subtracting the S&P 500 return from each security's return.
# 3. Calculate the linked rolling excess return for the past 15 days.
# 4. Calculate the linked rolling excess return for the past 60 days.
# 5. Calculate the ex-ante volatility for each day. Note that you should use all daily returns since the beginning of the sample up to each day.

# In[2]:


# Reading in the stock-prices csv file in first  
prices_df = pd.read_csv('stock-prices.csv')
# Changing the dataframe to date time index 
prices_df.index = pd.to_datetime(prices_df["date"],format="%Y%m%d")
# pivoted the dataframe to have the tickers as the column and the prices as the values 
prices_df = prices_df.pivot(columns = "TICKER" ,values = "PRC")
#prices_df
# Reading in the snp-prices csv file in second
snp_df = pd.read_csv('snp-prices.csv')
#snp_df
snp_df.index = pd.to_datetime(snp_df["DATE"],format = "%Y%m%d")
snp_df = snp_df.drop(columns = "DATE")
#snp_df
#Joined the two dataframes into one large dataframe 
df = prices_df.join(snp_df)
df = df.fillna(method ='ffill')
df.tail()


# Part 1 Data Preperation
# 1. Calculate returns on the prices for all assets (included the S&P 500).
# 2. Calculate returns in excess of the market return by subtracting the S&P 500 return from each security's return.
# 3. Calculate the linked rolling excess return for the past 15 days.
# 4. Calculate the linked rolling excess return for the past 60 days.
# 5. Calculate the ex-ante volatility for each day. Note that you should use all daily returns since the beginning of the sample up to each day.

# In[25]:


#1 Calculated Returns on the prices for all assets (including S&P 500)
returns = df.pct_change()



#2 Calculated returns in excess of the market return by subtracting the S&P 500 return from each security return
excess_returns = pd.DataFrame()
for col in returns.columns:
    excess_returns[col] = returns[col] - returns['spindx']
    
excess_returns.tail()


# In[4]:


#3 Calcluated the linked rolling excess returns for the past 15 days using lamda function
day15_linked_returns = excess_returns.rolling(15).apply(lambda x: (x+1).prod() - 1, raw = False)
day15_linked_returns.tail()     


# In[5]:


#4 Calculate the linked rolling excess returns for the past 60 days using lamda function
day60_linked_returns = excess_returns.rolling(60).apply(lambda x: (x+1).prod() -1, raw = False)
day60_linked_returns.tail()


# In[6]:


#5 Calculate the ex-ante volatility for each day. Note that you should use all daily returns since the beginning of the sample up to each day
def calc_volatility(r_series):
# vol stores the volatility series.
    vol = pd.Series(np.zeros(len(r_series)), index=r_series.index)
# Go through each time in the returns.
    for t in range(len(r_series)):
# Grab the relevant returns.
        r = r_series.iloc[range(t, 0, -1)]
# Calculate the exponential weighting terms.
        deltas = pd.Series([(60. / 61.)**j for j in range(t)]) 
# Set the deltas index to the r index to make the math easier.
        deltas.index = r.index
# Calculate exponentially weighted average returns.
        r_bar = ((1.-60./61.) * deltas * r).sum()
# Calculate the ex-ante volatility.
        vol[t] += (261.0 * (1.-60./61.) * deltas * (r.shift(1) - r_bar) ** 2).sum()

# Return the volatility series.
    return vol

excess_vol = pd.DataFrame()
for col in returns.columns:
    excess_vol[col] = calc_volatility(returns[col])
    
excess_vol.head()

excess_vol.to_csv("exante-vols.csv")


# Part 2 Algorithim Execution 
# 1. For each of the five securities (not the S&P 500) and each day, calculate the position you will take according to the following logic.
# If the 15 day rolling return is greater than the 60 day rolling return, take a positive position equal to forty percent of the day's ex-ante volatility.
# If the 15 day rolling return is less than the 60 day rolling return, take a negative position equal to forty percent of the day's ex-ante volatility.
# If they are equal, take a position of zero.
# 2. Calculate the change in your cash position for each security as a result of taking the position you took. Note that this is equal to ,
# where indexes a specific stock.
# 3. Calculate the total cash change for each day by adding up the cash changes for each day across each security. In a separate location, store the cumulative sum of all changes in cashflow -- this is your daily cash position.
# 4. Calculate each position's market value (daily) by multiplying the day's position by the price.
# 5. Calculate the total daily market value by adding all the position market values together.
# 6. Calculate the dollar-valued returns on each position by multiplying each stock's daily market value by stock's daily return.
# 7. Calculate the daily weights of each position in your total portfolio, which is given by the market value of a position divided by the total market value of your portfolio. Cash should also have a weighting -- a good way to get this is to have a single dataframe of your positions, with six columns. One for each security, and one for the cash position.
# 8. Calculate daily portfolio returns by multiplying each position's weight by the position's return. The cash position should be multiplied by the daily risk-free rate, which can be assumed to be 0.0001, or 0.01%.
# 9. Save a file as a .csv that displays your daily positions, weights, cash holdings, and total portfolio returns for each security (include cash). This needs to be turned in with your assignment.
# 
# 
# 
# Your trading strategy needs to report positions for securities that do not exist, and those positions should be zero. 

# In[7]:


#1 Calculate the position for 5 securities on each day 
# By comparing the day 15 linked return valeues to the day 60 linked return values
# becuase we are doing 60 day linked return there should be no positon taken for the first 60 days across all stocks.
position = day15_linked_returns > day60_linked_returns
position = position.drop(['spindx'], axis =1 )
# Replace all true values in with 1 
# Replace all false values with -1 
position = position.replace({True: 1, False : -1.0 })
#put zero for all 
position[pd.isna(day60_linked_returns)] = 0.0
position.tail()


# In[8]:


#For 1 take positive position, for - 1 take a negative position, for 0 take no position 
#All positions will have the same mathematical function where multiply the position by 0.40 of the excess volatility 
take_position = (excess_vol*0.40* position)
# we are not taking position for spindx so we can drop this column
take_position = take_position.drop(['spindx'], axis =1 )
take_position.tail()


# In[9]:


#2 Calculate the change in your cash position for each security 
# change in cash position is calculated by position shift above mines the position below times the price of the stock
cash_position = (take_position.shift(1) - take_position) * prices_df
cash_position.tail()


# In[10]:


# 3 Calculate the total cash change for each day by adding up the cash changes for each day across each security 
# use sum and cumsum function to add up each row and take cumulative sum 
total_cash_change = cash_position.sum(1).cumsum()
total_cash_change.tail()


# In[11]:


#4 Calculate each position's market value(daily) by multiplying the day's position by the price. 
# multiply position value and the days price and cash column to the data frame 
position_market_value = take_position * prices_df
position_market_value['Cash'] = total_cash_change
position_market_value.tail()


# In[12]:


#5 Calculate the total daily market value by adding all the positional market values together. 
#Make sure you add your cash position to the total to the get the correct daily market value 
# use sum(1) to add up all the rows for each day 
total_daily_market_value = (position_market_value.sum(1))

total_daily_market_value.tail()


# In[13]:


#6 Calculate the returns on each position by multiplying the market value by the stock return 
# multiply the stock on each position by return dataframe created earlier in part 1.
position_returns = (position_market_value * returns)
position_returns = position_returns.drop(['spindx'], axis =1)
position_returns.tail()


# In[14]:


#7 Calculate the daily weights of each position in your total portfolio, 
#  Divided the market value of each position divided by the total market value of the portfolio to get the daily weights of each secuirty with cash column
daily_weights_position_portfolio = position_market_value.divide(total_daily_market_value, axis = 0)
daily_weights_position_portfolio.tail()


# In[15]:


#8 Calculate daily portfolio returns 
#by multiplying each positions weight by the positions returns 
#cash position should be multiplied by the daily risk-free rate 
security_returns = returns.copy()
security_returns['Cash'] = 0.0001
daily_portfolio_returns = (daily_weights_position_portfolio * security_returns).sum(1)
# print out tail to see if returns are correct                                                                                 
daily_portfolio_returns.tail()


# In[16]:


#9 Save a file as a .csv 
#that displays your daily positions, weights, cash holdings, and total portfolio returns for each security 
daily_pos_csv = take_position.to_csv("daily_pos_csv")
weights_csv = daily_weights_position_portfolio.to_csv('weights_csv')
cash_holdings_csv =total_cash_change.to_csv('cash_holdings_csv')
total_portfolio_returns_csv = daily_portfolio_returns.to_csv('daily_portfolio_returns')


# Part 3 Diagnostics & Strategy Report 
# 1. Calculate your average portfolio return, and the standard deviation of your portfolio returns. Do the same for the S&P 500 returns.
# 2. Calculate the portfolio cumulative return for each day, by linking all previous and currentreturnstogether.Tocalculatethecumulativereturnattime ,youshouldlink together all daily portfolio returns from time to .
# 3. Calculate the S&P 500 cumulative return.
# 4. Calculate the Sharpe ratio for your portfolio, defined as the average of the portfolio's daily excess returns (defined as daily return minus the S&P 500 returns) divided by the variance of the portfolio's excess returns.
# 5. Using the above measures, write a (very brief!) summary of the trading strategy. Please address the following:
# Did this strategy perform well, relative to the S&P 500? Include a line graph showing the cumulative returns of your portfolio and the S&P 500 across time.
# Is the trading strategy highly risky? Discuss the Sharpe ratio, your portfolio's standard deviation of return relative to the market standard deviation, and
# Is it reasonable to have the cash position your strategy required across time? Make a line graph showing the cash position of your strategy across time. Discuss the feasbility of your short position (if any), keeping in mind that a negative cash position means cash is being borrowed.

# In[17]:


#1 Calculate your average portfolio return, and the standard deviation of your portfolio returns. 
#Do the same for the S&P 500 returns.
# use .mean and .stf function to calculate the mean and standard deviation of the portfolio and the snp returns 
print('Average Portfolio Return')
print(daily_portfolio_returns.mean())
print('Average Portfolio Standard Deviation')
print(daily_portfolio_returns.std())
print('Average SNP Return')
print(returns['spindx'].mean())
print('Standard Deviation SNP Return')
print(returns['spindx'].std())


# In[18]:


#2 Calculate the cumulative portfolio returns for each day, by linking all previous and current returns together. 
#  To calculate the cumulative return at the time T, link together all daily portfolio returns from time 0 - T
# use fillna and replace to calculate the correct cummulative daily portfolio returns 
cumm_daily_portfolio_return = daily_portfolio_returns.fillna(0.0).replace({np.nan:0.0, np.inf:0.0, -np.inf:0.0}) 
# add 1 to the cummulative returns and use cumprod function to multiply the values and subtract 1  
cumm_daily_portfolio_return = (cumm_daily_portfolio_return + 1).cumprod() - 1

cumm_daily_portfolio_return.tail()


# In[19]:


#3 Calculate the S&P 500 cummulative return
snp_cumm_return = returns['spindx'] + 1
# use cumprod and subtract 1 again to get the value for the snp cummulative return 
snp_cumm_return = snp_cumm_return.cumprod() - 1
snp_cumm_return.tail()


# In[20]:


#  4 Calculate the Sharpe Ratio for your portfolio 
#  Defined as the average of the portfolio's daily excess returns (defined as daily return minus the S&P 500 returns) 
#  Divided by the variance of the portfolio's excess returns.
x = daily_portfolio_returns - excess_returns['spindx']
sharpe_ratio = x.mean()/x.var()
sharpe_ratio


# # 5  Summary 
# The strategy does not perform well compared to the S&P 500  since its super risky. The standard deviation and mean of our portfolio doesn't not perform well compared to the S&P500.We take 40% percent of the ex-ante volatility regardless of whether it is postive or negative position, which washes so many of the potential gains or opportunities to make a profit. The sharpe ratio of the portfolio is 0.00718865007912632 which is sub-optimal becuase its below 1.  The mean and standard deviation of the portfolio's return are much more risky without much more reward than the S&P 500 return. Having the cash postion be 40% of the volatilty in excess returns over time is unreasonable becuase the marekt changes over time and the alogrithim needs to adjust. The line graph of the cash position indicates that the cash position drops significantly for sometime, and we are borrowing money to mainting our strategy. Which doesn't make sense since there are other positions which would be more profitable. The plots of the cummulative portfolio return, the snp 500 return, and the cash held are plotting below, respectively. 

# In[21]:


# 5  
cumm_daily_portfolio_return.plot()


# In[22]:


snp_cumm_return.plot()


# In[23]:


daily_portfolio_returns.plot()


# In[24]:


total_cash_change.plot()


#  

# In[ ]:




