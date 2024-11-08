# Riskstats



## Hurst
The constant \( c \) is often less commonly discussed than the Hurst exponent \( H \), but it provides useful insights into the *amplitude* or *scale* of the fluctuations within the time series. Here are some example interpretations of different values of \( c \) in relation to the scale of fluctuations.

### 1. **Small \( c \) Values (e.g., \( c < 0.5 \))**
   - **Interpretation:** When \( c \) is small, the time series tends to have smaller, less volatile fluctuations. This means that the time series values stay relatively close to the average or trend without large deviations.
   - **Example:** A time series with \( c = 0.3 \) and \( H = 0.7 \) might represent a market that is *trending persistently* but in a relatively stable manner, with smaller ups and downs around that trend. For example, this could describe a stable stock or bond with consistent, modest growth over time.

### 2. **Moderate \( c \) Values (e.g., \( c \approx 0.5 \) to \( c \approx 1 \))**
   - **Interpretation:** Moderate values of \( c \) indicate average-sized fluctuations in the time series. The series has a moderate level of volatility, where deviations from the mean or trend are noticeable but not extreme.
   - **Example:** A time series with \( c = 0.7 \) and \( H = 0.5 \) could describe a financial return series that follows a random walk (no long-term memory), but with moderate swings. This might be common in markets that are generally stable but with periodic, moderate price fluctuations—like major indices under normal market conditions.

### 3. **Large \( c \) Values (e.g., \( c > 1 \))**
   - **Interpretation:** A large \( c \) value indicates larger fluctuations or volatility within the time series. Such a time series shows substantial deviation from the mean or trend, often with more pronounced ups and downs.
   - **Example:** A time series with \( c = 1.5 \) and \( H = 0.3 \) could describe a mean-reverting market with high volatility. This might represent commodities or highly speculative assets, where prices frequently revert to a mean but with large swings in both directions.

### 4. **Very Large \( c \) Values (e.g., \( c > 2 \))**
   - **Interpretation:** When \( c \) is very high, the time series is extremely volatile, with significant fluctuations and deviations. This reflects a market where prices are highly unstable and can experience sharp, unpredictable changes.
   - **Example:** A time series with \( c = 2.5 \) and \( H = 0.5 \) could resemble a highly volatile stock or cryptocurrency with no persistent trend but considerable random fluctuations. These values might describe a turbulent period where prices are hard to predict and swing widely around an average.

### Summary
- **Small \( c \) (< 0.5):** Low volatility, stable series with small fluctuations.
- **Moderate \( c \) (0.5 to 1):** Average volatility, moderate fluctuations.
- **Large \( c \) (> 1):** High volatility, large fluctuations.
- **Very Large \( c \) (> 2):** Extreme volatility, very large fluctuations.

While \( H \) indicates the type of memory or trend in the series, \( c \) essentially scales that trend or behavior, showing how intense the fluctuations are. Combining these two values helps you assess both the *pattern* and *intensity* of the time series dynamics.