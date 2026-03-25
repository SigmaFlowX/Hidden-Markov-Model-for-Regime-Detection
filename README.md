Currently all the main work is in [notebook](notebooks/hmm_regime_detection.ipynb).

## Tools used:
1) pandas, numpy
2) hmm learn library
3) sklearn library for PCA and features scaling
4) Matpotlib and seaborn for visualizations

## What has been done as of today 
1) Historical IMOEX index candles obtained from MOEX API.
2) Some feature engineering: log returns, vol, rolling drowdowns; features scaling.
3) PCA to reduce the number of parameters
4) Trained HMM with different numbers of states and used BIC and AIC metrics to determine the optimal number.
5) Some final model analysys: transition matrix, expected regime durations.

 ## The future 
 The most interesting part would of course be the walk forward backtest of mean reversion and momentum strategies (and their symbiosis) using hmm model for regime detection. <br>
 However, I have some plans on building my own all-purpose backtesting engine that would be a perfect fit for this task. <br>
 When I actually build it, I am planning to return to this project and run some interesting backtests with it. 

