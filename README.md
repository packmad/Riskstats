# Riskstats


Work in progress...

## Hurst exponent [memory / persistence]

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


## Historical Value‑at‑Risk (VaR) [max expected loss (95%)]

It is a non‑parametric way to estimate how much a portfolio could lose, at a chosen confidence level, over a given horizon, by looking directly at its own past performance rather than assuming any particular return distribution.
VaR estimates the maximum expected loss (as a fraction of portfolio value) over a specific time horizon with a given confidence level (often 95% or 99%).
So it’s a measure of downside tail risk.

E.g., VaR = −0.0215 → about −2.15%.
This means: “With 95% confidence, the ETF won’t lose more than 2.15% in a day/week (depending on your time frame).”



## Expected Shortfall [Avg. loss beyond VaR]
Expected Shortfall (also called Conditional VaR) tells you the average loss beyond the VaR threshold; i.e., when things go really bad, how bad on average?
This is a stricter and more informative tail-risk measure than VaR.

E.g., ES = −0.0358 → about −3.58%

If losses exceed the VaR limit, you can expect the average loss to be about 3.6%.


## POT VaR / ES	[Tail risk via EVT]
This uses Extreme Value Theory (EVT), which models the tails of the return distribution more precisely by fitting a Generalized Pareto Distribution to large losses (or gains).



## Katz Fractal Dimension [Complexity]
The Katz fractal dimension quantifies the complexity or “roughness” of a time series.

## Max Drawdown	[peak-to-trough loss]
The largest observed peak-to-trough loss from the highest to lowest point in the series.

E.g, MDD = 0.3343 → about 33.4%.



## MFDFA Spectrum Widt [multifractality]

From Multifractal Detrended Fluctuation Analysis (MFDFA), it describes the degree of multifractality, i.e., how heterogeneous the scaling behavior of fluctuations is.

+ Narrow width (≈ 0): Monofractal — simple, single scaling exponent.

+ Wide width (> 0.4): Multifractal — complex, multiple time-scale dependencies.