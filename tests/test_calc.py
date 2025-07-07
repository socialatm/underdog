import unittest
from calc import calculate_payout_american_odds, calculate_implied_probability

class TestBettingCalculators(unittest.TestCase):
    """
    Test suite for the betting calculation functions in calc.py.
    """

    def test_calculate_payout_american_odds_underdog(self):
        """Test payout calculation for an underdog (positive odds)."""
        result = calculate_payout_american_odds(odds=150, bet_amount=100)
        self.assertDictEqual(result, {
            'profit': 150.00,
            'total_payout': 250.00,
            'odds_type': 'underdog',
            'bet_amount': 100
        })

    def test_calculate_payout_american_odds_favorite(self):
        """Test payout calculation for a favorite (negative odds)."""
        result = calculate_payout_american_odds(odds=-110, bet_amount=100)
        self.assertAlmostEqual(result['profit'], 90.91)
        self.assertAlmostEqual(result['total_payout'], 190.91)
        self.assertEqual(result['odds_type'], 'favorite')

    def test_calculate_payout_american_odds_custom_bet(self):
        """Test payout calculation with a custom bet amount."""
        result = calculate_payout_american_odds(odds=200, bet_amount=50)
        self.assertEqual(result['profit'], 100.00)
        self.assertEqual(result['total_payout'], 150.00)

    def test_calculate_payout_american_odds_zero_odds(self):
        """Test that zero odds raise a ValueError."""
        with self.assertRaisesRegex(ValueError, "Odds cannot be zero"):
            calculate_payout_american_odds(odds=0, bet_amount=100)

    def test_calculate_implied_probability_underdog(self):
        """Test implied probability for an underdog (positive odds)."""
        self.assertAlmostEqual(calculate_implied_probability(100), 50.00)
        self.assertAlmostEqual(calculate_implied_probability(200), 33.33)

    def test_calculate_implied_probability_favorite(self):
        """Test implied probability for a favorite (negative odds)."""
        self.assertAlmostEqual(calculate_implied_probability(-110), 52.38)
        self.assertAlmostEqual(calculate_implied_probability(-200), 66.67)

    def test_calculate_implied_probability_zero_odds(self):
        """Test implied probability for zero odds."""
        # The current implementation's `else` block handles odds <= 0.
        # For odds = 0, probability is abs(0) / (abs(0) + 100) * 100 = 0.
        self.assertAlmostEqual(calculate_implied_probability(0), 0.00)


if __name__ == '__main__':
    # To run the tests, execute this file from your terminal:
    # python -m unittest discover
    unittest.main()
