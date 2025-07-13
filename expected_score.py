import math

def calculate_expected_score(rating_a, rating_b):
  """
  Calculates the expected score (as a percentage) for player A against player B
  based on their Elo ratings.
  """
  # Constant (usually 400)
  c = 400

  # Calculate Qa and Qb
  qa = 10**(rating_a / c)
  qb = 10**(rating_b / c)

  # Calculate the expected score
  expected_score_a = qa / (qa + qb)

  return expected_score_a * 100  # Return as a percentage

# Example usage:
rating_a = 2801
rating_b = 2726

expected_percentage = calculate_expected_score(rating_a, rating_b)

print(f"Player A's expected score against Player B: {expected_percentage:.2f}%")

expected_percentage = calculate_expected_score(rating_b, rating_a)

print(f"Player B's expected score against Player A: {expected_percentage:.2f}%")