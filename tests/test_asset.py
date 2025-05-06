import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

import numpy as np
import pandas as pd

from asset import Asset


class TestAsset(unittest.TestCase):
    """Unit-tests for the Asset analytics class."""

    def setUp(self):
        # Synthetic 4-day price series we can verify by hand
        self.prices = pd.Series([100, 110, 90, 120], name="Close")
        self.history_df = pd.DataFrame({"Close": self.prices})
        self.ticker = "TEST"
        self.name = "Test Asset"
        self.asset = Asset(self.ticker, self.name)

        # Put the CSV in a temporary directory so we never touch a real DB_DIR
        self.tmp_csv = Path(__file__).with_suffix(".csv")
        self.asset.db_file = str(self.tmp_csv)            # overwrite path used internally

    # ------------------------------------------------------------------ #
    #  get_history
    # ------------------------------------------------------------------ #

    @patch(f"{Asset.__module__}.isfile", return_value=True)
    @patch(f"{Asset.__module__}.pd.read_csv")
    def test_get_history_reads_local_csv(self, mock_read_csv, mock_isfile):
        """Reads from disk when the CSV is already present."""
        mock_read_csv.return_value = self.history_df

        hist1 = self.asset.get_history()
        hist2 = self.asset.get_history()           # second call must hit the cache

        self.assertIs(hist1, self.history_df)
        self.assertIs(hist2, self.history_df)
        mock_read_csv.assert_called_once_with(self.asset.db_file)   # only once thanks to the cache

    # ------------------------------------------------------------------ #
    #  Basic price-series helpers
    # ------------------------------------------------------------------ #

    def _prime_history_cache(self):
        """Helper: put our synthetic DataFrame straight into the cache."""
        self.asset.history = self.history_df.copy()

    def test_get_closing_prices(self):
        self._prime_history_cache()
        closes = self.asset.get_closing_prices()
        pd.testing.assert_series_equal(closes, self.prices)

    def test_simple_returns(self):
        self._prime_history_cache()
        expected = [0.1, -0.182, 0.333]
        got = [round(num, 3) for num in self.asset.get_simple_returns().to_list()]
        self.assertEqual(got, expected)

    def test_log_returns(self):
        self._prime_history_cache()
        expected = [0.095, -0.201, 0.288]
        got = [round(num, 3) for num in self.asset.get_log_returns().to_list()]
        self.assertEqual(got, expected)

    # ------------------------------------------------------------------ #
    #  Risk metrics that do their own stats
    # ------------------------------------------------------------------ #

    def test_historical_var_and_expected_shortfall(self):
        self._prime_history_cache()
        logret = np.log(self.prices).diff().dropna()
        alpha = 0.025
        expected_var = np.quantile(logret, alpha)
        expected_es = logret[logret <= expected_var].mean()

        self.assertAlmostEqual(self.asset.historical_var(alpha), expected_var)
        self.assertAlmostEqual(self.asset.expected_shortfall(alpha), expected_es)

    def test_maximum_drawdown(self):
        self._prime_history_cache()
        cm = np.maximum.accumulate(self.prices)
        expected_dd = (1.0 - self.prices / cm).max()
        self.assertAlmostEqual(self.asset.maximum_drawdown(), expected_dd)

    # ------------------------------------------------------------------ #
    #  Heavy stats (Hurst, POT, Katz, MF-DFA) – just check plumbing
    # ------------------------------------------------------------------ #

    @patch(f"{Asset.__module__}.compute_Hc", return_value=(0.55, None, []))
    def test_get_hurst_returns_scalar(self, mock_hc):
        self._prime_history_cache()
        h, _, _ = self.asset.get_hurst()
        self.assertEqual(h, 0.55)
        mock_hc.assert_called_once()

    @patch(f"{Asset.__module__}.genpareto.fit", return_value=(0.2, 0.0, 1.0))
    @patch(f"{Asset.__module__}.genpareto.ppf", return_value=0.1)
    def test_pot_var_es_shapes(self, mock_ppf, mock_fit):
        self._prime_history_cache()
        var, es = self.asset.pot_var_es(alpha=0.05, threshold_quantile=0.90)
        # Just verify they are floats and ppf/fit were invoked
        self.assertIsInstance(var, float)
        self.assertIsInstance(es, float)
        mock_fit.assert_called_once()
        mock_ppf.assert_called_once()

    # ------------------------------------------------------------------ #
    #  toJSON aggregation (smoke test with all heavy bits mocked)
    # ------------------------------------------------------------------ #

    @patch.object(Asset, "mfdfa_spectrum_width", return_value=1.23)
    @patch.object(Asset, "maximum_drawdown", return_value=0.10)
    @patch.object(Asset, "katz_fractal_dimension", return_value=1.5)
    @patch.object(Asset, "pot_var_es", return_value=(-0.08, -0.12))
    @patch.object(Asset, "expected_shortfall", return_value=-0.06)
    @patch.object(Asset, "historical_var", return_value=-0.05)
    @patch.object(Asset, "get_hurst", return_value=(0.55, None, []))
    def test_toJSON_contains_all_keys(self, *_):
        self._prime_history_cache()
        info = self.asset.toJSON()
        expected_keys = {
            "ticker",
            "name",
            "hurst_exponent",
            "historical_var",
            "expected_shortfall",
            "Peaks-Over-Threshold VaR and ES",
            "katz_fractal_dimension",
            "maximum_drawdown",
            "mfdfa_spectrum_width",
        }
        self.assertEqual(set(info.keys()), expected_keys)
        self.assertEqual(info["ticker"], self.ticker)
        self.assertEqual(info["name"], self.name)


if __name__ == "__main__":          # pragma: no cover
    unittest.main(verbosity=2)
