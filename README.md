# Riskstats

Attribution: the code for the Hurst's exponent is taken from https://github.com/Mottl/hurst


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


The constant c is a scaling factor related to the amplitude or “scale” of fluctuations in the time series. 
While H reflects the pattern or structure of the series, c gives additional context to the magnitude of these fluctuations.
Unlike H, the constant c is not directly tied to the type of correlation (i.e., persistence or mean reversion), but rather to the intensity of the changes.
A larger c indicates larger fluctuations in absolute terms, while a smaller c suggests smaller fluctuations.

Interpretation of Hurst constant c:

+ Small (c<0.5): Low volatility, small fluctuations.
+ Moderate (0.5<c<1): Average volatility, moderate fluctuations.
+ Large (c>1): High volatility, large fluctuations.
+ Very Large (c>2): Extreme volatility, very large fluctuations.

