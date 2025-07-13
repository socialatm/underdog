def calculate_implied_probability(american_odds: int) -> float:
    """
    Calculates the implied probability from American odds.

    Args:
        american_odds: The American odds value (e.g., -110, +250).

    Returns:
        The implied probability as a float (e.g., 0.5238 for -110).
        Returns 0.0 if the odds are zero, which is an invalid input.
    """
    if american_odds == 0:
        return 0.0

    if american_odds > 0:
        # Formula for positive (underdog) odds
        return 100 / (american_odds + 100)
    else:  # american_odds < 0
        # Formula for negative (favorite) odds
        return abs(american_odds) / (abs(american_odds) + 100)


def remove_vig(market_odds: list[int]) -> list[float]:
    """
    Calculates the no-vig or "true" probability for a set of market odds.

    Args:
        market_odds: A list of American odds for all outcomes in a market
                     (e.g., [-110, -110] for a 2-way market).

    Returns:
        A list of floats representing the true probability for each outcome.
        Returns an empty list if the input is empty.
    """
    if not market_odds:
        return []

    # 1. Calculate the implied probability for each outcome
    implied_probabilities = [calculate_implied_probability(odds) for odds in market_odds]

    # 2. Sum the probabilities to find the total market percentage (overround)
    total_market_percentage = sum(implied_probabilities)

    # If the total is <= 1, there's no vig to remove or it's a perfect market
    if total_market_percentage <= 1.0:
        return implied_probabilities

    # 3. Normalize each probability by dividing by the total percentage
    true_probabilities = [prob / total_market_percentage for prob in implied_probabilities]

    return true_probabilities


# --- Example Usage ---

# Example 1: A 2-way moneyline market
moneyline_market = [-250, +230]
true_probs_ml = remove_vig(moneyline_market)

print("--- Moneyline Market (-250 / +230) ---")
implied_ml = [calculate_implied_probability(o) for o in moneyline_market]
print(f"Implied Probabilities: {[f'{p:.2%}' for p in implied_ml]}")
print(f"True Probabilities:    {[f'{p:.2%}' for p in true_probs_ml]}")
print(f"Sum of True Probs: {sum(true_probs_ml):.4f}\n")

# Example 2: A 3-way soccer market (Team A Win / Draw / Team B Win)
soccer_market = [+150, +240, +180]
true_probs_soccer = remove_vig(soccer_market)

print("--- 3-Way Soccer Market (+150 / +240 / +180) ---")
implied_soccer = [calculate_implied_probability(o) for o in soccer_market]
print(f"Implied Probabilities: {[f'{p:.2%}' for p in implied_soccer]}")
print(f"True Probabilities:    {[f'{p:.2%}' for p in true_probs_soccer]}")
print(f"Sum of True Probs: {sum(true_probs_soccer):.4f}")