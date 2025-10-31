from typing import Tuple, List, Dict, Optional

import json
import warnings
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from os.path import join, isfile, isdir, dirname, abspath
from typing import Sequence
from scipy.stats import genpareto

from hurst import hurst_rs


script_dir = dirname(abspath(__file__))
DB_DIR = join(script_dir, "DBcsv")


class Asset:
    def __init__(self, ticker_symbol: str, name: str):
        self.ticker_symbol = ticker_symbol
        self.db_file = join(DB_DIR, f'{ticker_symbol}.csv')
        self.name = name
        self.history = None
        self.log_returns = None
        self.simple_returns = None

    def get_history(self) -> pd.DataFrame:
        if self.history is not None:
            return self.history
        if not isfile(self.db_file):
            yf_history = yf.Ticker(self.ticker_symbol).history(period="max", interval="1d", raise_errors=True)
            yf_history.to_csv(self.db_file)
        self.history = pd.read_csv(self.db_file)
        assert self.history is not None
        return self.history

    def get_closing_prices(self) -> pd.Series:
        return self.get_history()['Close'].dropna()

    def get_simple_returns(self)-> pd.Series:
        if self.simple_returns is not None:
            return self.simple_returns
        self.simple_returns = self.get_closing_prices().pct_change().dropna()
        return self.simple_returns

    def get_log_returns(self) -> pd.Series:
        if self.log_returns is not None:
            return self.log_returns
        self.log_returns = np.log(self.get_closing_prices()).diff().dropna()
        return self.log_returns

    # -----------------------------------------------------------------------------
    #  Long‑memory & fractal diagnostics
    # -----------------------------------------------------------------------------

    def get_hurst(self) -> float:
        s_no_zeros = self.get_simple_returns()[self.get_simple_returns() != 0]
        return float(hurst_rs(s_no_zeros))

    def katz_fractal_dimension(self) -> float:
        """Katz fractal dimension of a *curve* x (often prices)."""
        x = np.asarray(self.get_log_returns(), dtype=float)
        # total path length L and diameter d
        L = np.sum(np.abs(np.diff(x)))
        d = np.max(np.abs(x - x[0]))
        if d == 0:
            return 1.0
        n = len(x)
        return float(np.log10(n) / (np.log10(d / L) + np.log10(n)))

    # -----------------------------------------------------------------------------
    #  Fat‑tail / tail‑risk metrics
    # -----------------------------------------------------------------------------

    def historical_var(self, alpha: float = 0.025) -> float:
        """Empirical (historical) VaR at level *alpha*; alpha = 0.025 ⇒ 97.5% VaR."""
        return float(np.quantile(self.get_log_returns(), alpha))

    def expected_shortfall(self, alpha: float = 0.025) -> float:
        """CVaR / ES at level *alpha*: mean of returns ≤ VaR_alpha."""
        var_alpha = self.historical_var(alpha)
        logret = self.get_log_returns()
        tail = logret[logret <= var_alpha]
        return float(tail.mean())

    def pot_var_es(
            self,
            alpha: float = 0.025,  # target left‑tail probability (e.g. 0.025 → 97.5% left‑tail)
            threshold_quantile: float = 0.90,  # quantile that defines the POT threshold u (e.g. 0.90)
    ) -> Tuple[float, float]:
        r = self.get_log_returns()
        u = np.quantile(r, threshold_quantile)
        excesses = u - r[r <= u]  # losses are negative; flip sign so excesses > 0
        if len(excesses) < 50:
            warnings.warn("Fewer than 50 tail exceedances – GPD fit may be unstable.")
        # Fit GPD to *positive* excesses
        c, loc, scale = genpareto.fit(excesses, floc=0)
        # Tail exceedance prob.
        p_exceed = alpha / (1 - threshold_quantile)
        # VaR from inverse CDF of fitted GPD, then convert back to return sign
        var = u - genpareto.ppf(p_exceed, c, loc=0, scale=scale)
        # ES formula for GPD tail
        if c >= 1:
            es = np.nan  # mean diverges
        else:
            es = var + (scale - c * (u - var)) / (1 - c)
        return float(var), float(es)

    # -----------------------------------------------------------------------------
    #  Drawdown‑based metric
    # -----------------------------------------------------------------------------

    def maximum_drawdown(self) -> float:
        """Maximum drawdown for a price series *px* (as a *positive* fraction)."""
        px = self.get_closing_prices()
        if not np.all(px > 0):
            raise ValueError("Input must be price levels (strictly positive).")
        cumulative_max = np.maximum.accumulate(px)
        drawdowns = 1.0 - px / cumulative_max
        return float(drawdowns.max())

    # -----------------------------------------------------------------------------
    #  Multifractal spectrum width (Δα) using a minimalist MF‑DFA
    # -----------------------------------------------------------------------------

    def mfdfa_spectrum_width(
            self,
            qs: Sequence[float] = (-5, -3, -1, 0, 1, 3, 5),
            scale_min: int = 16,
            scale_max: int = 1024,
            scale_ratio: float = 2.0,
            eps: float = 1e-12,  # ⟨NEW⟩ safeguard for F2 = 0
    ) -> float:
        """
        Width of the multifractal spectrum (α_max − α_min) via a light MF‑DFA.

        • Handles q = 0 explicitly (geometric mean → no 1/0 warning)
        • Adds a small ε to F² to keep 0^(negative q/2) from blowing up
        """
        # ---------- profile ----------
        r = self.get_log_returns()
        y = np.cumsum(r - r.mean())

        # ---------- scales ----------
        scales = []
        s = scale_min
        while s <= scale_max:
            scales.append(int(s))
            s *= scale_ratio
        scales = np.asarray(scales)

        # ---------- fluctuation functions ----------
        qs_arr = np.asarray(qs, dtype=float)
        Fq = np.zeros((len(qs_arr), len(scales)))

        for j, s in enumerate(scales):
            segments = len(y) // s
            if segments < 2:
                continue

            for v in range(segments):
                seg = y[v * s:(v + 1) * s]
                t = np.arange(s)

                # local detrending (order‑1 polynomial)
                coeffs = np.polyfit(t, seg, 1)
                trend = np.polyval(coeffs, t)
                res = seg - trend

                # local variance  F²
                F2 = np.mean(res ** 2) + eps  # ⟨NEW⟩ add ε once

                # accumulate for all q
                for i, q in enumerate(qs_arr):
                    if q == 0:
                        # geometric mean
                        Fq[i, j] += np.exp(0.5 * np.mean(np.log(res ** 2 + eps)))
                    else:
                        Fq[i, j] += F2 ** (q / 2)

            # ---------- average over segments ----------
            valid = Fq[:, j] > 0
            if not valid.any():
                continue

            Fq[valid, j] /= segments

            # exponentiation step (1/q) only where q ≠ 0
            nz = valid & (qs_arr != 0)
            if nz.any():
                Fq[nz, j] = Fq[nz, j] ** (1.0 / qs_arr[nz])
            # q = 0 rows already correct

        # ---------- log‑log regression → H(q) ----------
        log_scales = np.log(scales)
        Hq = np.full(len(qs_arr), np.nan)

        for i in range(len(qs_arr)):
            mask = Fq[i] > 0
            if mask.sum() < 2:
                continue
            coeffs = np.polyfit(log_scales[mask], np.log(Fq[i, mask]), 1)
            Hq[i] = coeffs[0]

        # ---------- spectrum width ----------
        finite = np.isfinite(Hq)
        if finite.sum() < 2:
            warnings.warn("Not enough scales/qs for reliable MF‑DFA; returning NaN.")
            return np.nan

        qs_f, Hq_f = qs_arr[finite], Hq[finite]
        tq = qs_f * Hq_f - 1
        alpha = np.gradient(tq, qs_f)

        return float(alpha.max() - alpha.min())

    # -----------------------------------------------------------------------------
    
    def toJSON(self) -> Dict:
        return {
            'ticker': self.ticker_symbol,
            'name': self.name,
            'Hurst exponent': self.get_hurst(),
            'Historical Value-at-Risk (VaR 97.5%)': self.historical_var(),
            'Expected Shortfall (ES)': self.expected_shortfall(),
            'Peaks-over-Threshold (POT) VaR and ES': self.pot_var_es(),
            'Katz Fractal Dimension': self.katz_fractal_dimension(),
            'Maximum Drawdown': self.maximum_drawdown(),
            'MFDFA Spectrum Width': self.mfdfa_spectrum_width(),
        }

    def __repr__(self):
        return json.dumps(self.toJSON(), indent=4)

