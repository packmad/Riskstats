import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import linregress


"""
Hurst exponent and RS-analysis
https://en.wikipedia.org/wiki/Hurst_exponent
https://en.wikipedia.org/wiki/Rescaled_range
"""


def hurst_rs(series, min_window=8, max_window=None, step=1):
    """
    Estimate the Hurst exponent H (0 < H < 1) of a 1‑D sequence
    using rescaled‑range (R/S) analysis.

    Parameters
    ----------
    series : array_like
        1‑D array or list containing the time‑series values.
    min_window : int, optional
        Smallest window size (>= 8 is typical). Default is 8.
    max_window : int or None, optional
        Largest window size checked.  If None, uses len(series)//2.
    step : int, optional
        Increment in window size when sweeping. Default is 1.

    Returns
    -------
    H : float
        Estimated Hurst exponent.
    """
    x = np.asarray(series, dtype=np.float64)
    n = x.size
    if n < min_window * 2:
        raise ValueError("Series too short for chosen min_window")

    max_window = max_window or n // 2

    # Candidate window sizes t
    windows = np.arange(min_window, max_window + 1, step, dtype=int)
    rs_vals = []

    # Compute (R/S)_t for each window length t
    for t in windows:
        # generate all sliding blocks of length t
        blocks = sliding_window_view(x, t)
        # mean‑center each block
        centered = blocks - blocks.mean(axis=1, keepdims=True)
        # cumulative deviate for each block
        z = centered.cumsum(axis=1)
        # range R
        R = z.max(axis=1) - z.min(axis=1)
        # std‑dev S
        S = centered.std(axis=1, ddof=1)
        # avoid division by zero
        RS = R / S
        RS = RS[~np.isnan(RS) & np.isfinite(RS) & (S > 0)]
        if RS.size:
            rs_vals.append(RS.mean())

    if len(rs_vals) < 2:
        raise RuntimeError("Not enough windows with finite (R/S) values")

    # linear regression in log‑log space
    log_t = np.log(windows[:len(rs_vals)])
    log_rs = np.log(rs_vals)
    slope, _, _, _, _ = linregress(log_t, log_rs)

    return float(slope)
