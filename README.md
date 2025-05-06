# Riskstats




## Hurst 

The Hurst exponent H is a measure of the tendency of a time series to either persist in a trend, revert to the mean, or exhibit random (Brownian) behavior. 

Interpretation of Hurst exponent H:

+ If H<0.5: The time series shows negative autocorrelation or mean reversion. If it has been increasing, it is likely to reverse and start decreasing, and vice versa. A low H value indicates that the series is "mean-reverting."
  + For example, H≈0.3 might suggest that large deviations from the mean are likely to be corrected over time.
  + H < 0: This is less common and suggests an extreme form of anti-persistence or noise.
  
+ If H=0.5: The time series follows a random walk, similar to a classic Brownian motion. There is no long-term dependence, and past values do not influence future values. 
  + Financial returns often have H≈0.5, indicating random behavior.

+ If H>0.5: The time series exhibits positive autocorrelation or trend persistence. This means that if the time series has been increasing, it is likely to continue increasing, and if it has been decreasing, it is likely to continue decreasing. In other words, the series has a tendency to follow a trend. 
  + For example, H≈0.7 might suggest a trending market with some degree of predictability.
  + If H>1: Indicates a time series with long-term memory (super-diffusive behavior).


## Historical Value‑at‑Risk (VaR)

It is a non‑parametric way to estimate how much a portfolio could lose, at a chosen confidence level, over a given horizon, by looking directly at its own past performance rather than assuming any particular return distribution.

