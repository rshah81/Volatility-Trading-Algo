# Volatility-Trading-Algo
Simple Volatility Based Trading Algorithm for 5 stocks vs the SP 500 index 
Part 1 - Data Preparation
1. Calculate returns on the prices for all assets (included the S&P 500).
2. Calculate returns in excess of the market return by subtracting the S&P 500 returnfrom each security's return.
3. Calculate the linked rolling excess return for the past 15 days.
4. Calculate the linked rolling excess return for the past 60 days.
5. Calculate the ex-ante volatility for each day. Note that you should use all daily returnssince the beginning of the sample up to each day.

Part 2 - Algorithm Execution
1. For each of the five securities (not the S&P 500) and each day, calculate the position you will take according to the following logic.
  If the 15 day rolling return is greater than the 60 day rolling return, take apositive position equal to forty percent of the day's ex-ante volatility.
  If the 15 day rolling return is less than the 60 day rolling return, take a negativeposition equal to forty percent of the day's ex-ante volatility.
  If they are equal, take a position of zero.
2. Calculate the change in your cash position for each security as a result of taking the position you took. 
3. Calculate the total cash change for each day by adding up the cash changes for eachday across each security. In a separate location, store the cumulative sum of allchanges in cashflow -- this is your daily cash position.
4. Calculate each position's market value (daily) by multiplying the day's position by theprice.
5. Calculate the total daily market value by adding all the position market valuestogether.
6. Calculate the dollar-valued returns on each position by multiplying each stock's dailymarket value by stock's daily return.
7. Calculate the daily weights of each position in your total portfolio, which is given bythe market value of a position divided by the total market value of your portfolio.Cash should also have a weighting -- a good way to get this is to have a singledataframe of your positions, with six columns. One for each security, and one for thecash position.
8. Calculate daily portfolio returns by multiplying each position's weight by theposition's return. The cash position should be multiplied by the daily risk-free rate,which can be assumed to be 0.0001, or 0.01%.
9. Save file as a .csv that displays your daily positions, weights, cash holdings, andtotal portfolio returns for each security (include cash).

Part 3 - Diagnostics & Strategy Report
1. Calculate your average portfolio return, and the standard deviation of your portfolioreturns. Do the same for the S&P 500 returns.
2. Calculate the portfolio cumulative return for each day, by linking all previous andcurrent returns together. To calculate the cumulative return at time t, you should linktogether all daily portfolio returns from time 0 to t.
3. Calculate the S&P 500 cumulative return.
4. Calculate the Sharpe ratio for your portfolio, defined as the average of the portfolio'sdaily excess returns (defined as daily return minus the S&P 500 returns) divided bythe variance of the portfolio's excess returns.
