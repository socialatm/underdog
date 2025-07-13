import math

def generate_elo(player_rating: int, opponent_rating: int, score: float, k_factor: int = 32) -> int:
    """
    Calculates and returns a player's new Elo rating after a single match.

    Args:
        player_rating: The current Elo rating of the player.
        opponent_rating: The current Elo rating of the opponent.
        score: The result of the match from the player's perspective.
               1.0 for a win, 0.5 for a draw, 0.0 for a loss.
        k_factor: The K-factor, which determines how much the rating changes.
                  Higher values mean more volatile ratings. Common values are
                  16 (for masters) or 32 (for newer players).

    Returns:
        The player's new Elo rating, rounded to the nearest integer.
    """
    # 1. Calculate the expected score for the player
    # This formula gives the probability of the player winning against the opponent.
    expected_score = 1 / (1 + math.pow(10, (opponent_rating - player_rating) / 400))

    # 2. Calculate the new rating
    # The new rating is the old rating plus the K-factor multiplied by the
    # difference between the actual score and the expected score.
    new_rating = player_rating + k_factor * (score - expected_score)

    return round(new_rating)

# --- Example Usage ---

# Player A (1500 Elo) plays against Player B (1700 Elo)
player_a_elo = 1500
player_b_elo = 1700

print(f"Initial Ratings -> Player A: {player_a_elo}, Player B: {player_b_elo}\n")

# --- Scenario 1: Player A (the underdog) wins ---
# Player A's score is 1.0, Player B's score is 0.0
new_player_a_elo = generate_elo(player_a_elo, player_b_elo, 1.0)
new_player_b_elo = generate_elo(player_b_elo, player_a_elo, 0.0)

print(f"After A wins -> Player A: {new_player_a_elo}, Player B: {new_player_b_elo}")
print(f"Player A gained {new_player_a_elo - player_a_elo} points.")
print(f"Player B lost {player_b_elo - new_player_b_elo} points.\n")

# --- Scenario 2: Player B (the favorite) wins ---
# Player A's score is 0.0, Player B's score is 1.0
new_player_a_elo = generate_elo(player_a_elo, player_b_elo, 0.0)
new_player_b_elo = generate_elo(player_b_elo, player_a_elo, 1.0)

print(f"After B wins -> Player A: {new_player_a_elo}, Player B: {new_player_b_elo}")
print(f"Player A lost {player_a_elo - new_player_a_elo} points.")
print(f"Player B gained {player_b_elo - new_player_b_elo} points.")