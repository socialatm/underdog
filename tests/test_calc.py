import pytest
from calc import calculate_payout_american_odds, calculate_implied_probability


def test_calculate_payout_american_odds_underdog():
    """Test payout calculation for an underdog (positive odds)."""
    result = calculate_payout_american_odds(odds=150, bet_amount=100)
    assert result == {
        'profit': 150.00,
        'total_payout': 250.00,
        'odds_type': 'underdog',
        'bet_amount': 100
    }

def test_calculate_payout_american_odds_favorite():
    """Test payout calculation for a favorite (negative odds)."""
    result = calculate_payout_american_odds(odds=-110, bet_amount=100)
    assert result['profit'] == pytest.approx(90.91)
    assert result['total_payout'] == pytest.approx(190.91)
    assert result['odds_type'] == 'favorite'

def test_calculate_payout_american_odds_custom_bet():
    """Test payout calculation with a custom bet amount."""
    result = calculate_payout_american_odds(odds=200, bet_amount=50)
    assert result['profit'] == 100.00
    assert result['total_payout'] == 150.00

def test_calculate_payout_american_odds_zero_odds():
    """Test that zero odds raise a ValueError."""
    with pytest.raises(ValueError, match="Odds cannot be zero"):
        calculate_payout_american_odds(odds=0, bet_amount=100)

def test_calculate_implied_probability_underdog():
    """Test implied probability for an underdog (positive odds)."""
    assert calculate_implied_probability(100) == pytest.approx(50.00)
    assert calculate_implied_probability(200) == pytest.approx(33.33)

def test_calculate_implied_probability_favorite():
    """Test implied probability for a favorite (negative odds)."""
    assert calculate_implied_probability(-110) == pytest.approx(52.38)
    assert calculate_implied_probability(-200) == pytest.approx(66.67)

def test_calculate_implied_probability_zero_odds():
    """Test implied probability for zero odds."""
    # The current implementation's `else` block handles odds <= 0.
    # For odds = 0, probability is abs(0) / (abs(0) + 100) * 100 = 0.
    assert calculate_implied_probability(0) == pytest.approx(0.00)