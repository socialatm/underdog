import pandas as pd
import os

def calculate_payout_american_odds(odds, bet_amount=100):
    """
    Calculate payout from American betting odds
    
    Args:
        odds (int): American odds (positive for underdogs, negative for favorites)
        bet_amount (float): Amount wagered (default $100)
    
    Returns:
        dict: Contains profit, total_payout, and odds_type
    """
    if odds > 0:  # Underdog odds (positive)
        profit = (odds / 100) * bet_amount
        odds_type = "underdog"
    elif odds < 0:  # Favorite odds (negative)
        profit = (100 / abs(odds)) * bet_amount
        odds_type = "favorite"
    else:
        raise ValueError("Odds cannot be zero")
    
    total_payout = bet_amount + profit
    
    return {
        'profit': round(profit, 2),
        'total_payout': round(total_payout, 2),
        'odds_type': odds_type,
        'bet_amount': bet_amount
    }

def calculate_implied_probability(odds):
    """
    Calculate implied probability from American odds
    
    Args:
        odds (int): American odds
    
    Returns:
        float: Implied probability as percentage
    """
    if odds > 0:  # Underdog
        probability = 100 / (odds + 100) * 100
    else:  # Favorite
        probability = abs(odds) / (abs(odds) + 100) * 100
    
    return round(probability, 2)

def main():
    """Extract data from table_98_percent_first4.csv into a pandas DataFrame"""
    
    # Define the CSV file path
    csv_file = "table_98_percent_first4.csv"
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' not found in the current directory.")
        return None
    
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)
        
        # Display basic information about the DataFrame
        print(f"Successfully loaded data from '{csv_file}'")
        
        return df
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    # Load the data
    dataframe = main()
    
    # You can perform additional operations on the dataframe here
    if dataframe is not None:
        print(f"\nDataFrame loaded successfully with {len(dataframe)} rows and {len(dataframe.columns)} columns")

        favorite_wins = dataframe['Favourite Wins'].sum()
        print(f"\nTotal favorite wins: {favorite_wins}")

        underdog_wins = dataframe['Underdog Wins'].sum()
        print(f"Total underdog wins: {underdog_wins}")

        # Calculate the percentage of underdog wins
        underdog_percentage = (underdog_wins / (favorite_wins + underdog_wins)) * 100
        print(f"Percentage of underdog wins: {underdog_percentage:.2f}%")
        
        # minimum number of underdog wins
        min_underdog_wins = dataframe['Underdog Wins'].min()
        print(f"\nMinimum number of underdog wins: {min_underdog_wins}")

        # maximum number of underdog wins
        max_underdog_wins = dataframe['Underdog Wins'].max()
        print(f"Maximum number of underdog wins: {max_underdog_wins}")
        
        total_events = len(dataframe)
        print(f"Total number of events: {total_events}")
        print(f"\n")

        # CORRECTED: Calculate events with underdog wins >= min_underdog_wins
        events_gte_min = len(dataframe[dataframe['Underdog Wins'] >= min_underdog_wins])
        print(f"Total number of events with {min_underdog_wins} or more underdog wins: {events_gte_min}")
        print(f"\n")

        # create a loop from min_underdog_wins to max_underdog_wins
        for i in range(min_underdog_wins, max_underdog_wins + 1):
            count = len(dataframe[dataframe['Underdog Wins'] == i])
            # calculate the percentage of events with i underdog wins
            percent_i_underdog_wins = (count / events_gte_min) * 100
            print(f"Percentage of events with {i} underdog wins: {percent_i_underdog_wins:.2f}%")

        # Example payout calculations for underdog betting
        print(f"\n{'='*50}")
        print("UNDERDOG BETTING PAYOUT EXAMPLES")
        print(f"{'='*50}")
        
        # Common underdog odds examples
        underdog_odds_examples = [+150, +200, +250, +300, +400, +500]
        bet_amount = 100
        
        print(f"Bet Amount: ${bet_amount}")
        print(f"{'Odds':<8} {'Profit':<10} {'Total Payout':<15} {'Implied Prob':<15}")
        print("-" * 50)
        
        for odds in underdog_odds_examples:
            payout_info = calculate_payout_american_odds(odds, bet_amount)
            implied_prob = calculate_implied_probability(odds)
            print(f"{odds:+8} ${payout_info['profit']:<9} ${payout_info['total_payout']:<14} {implied_prob}%")
        
        # Calculate potential returns based on your underdog win percentage
        print(f"\n{'='*50}")
        print("POTENTIAL RETURNS BASED ON YOUR DATA")
        print(f"{'='*50}")
        
        # Using your calculated underdog percentage as win rate
        win_rate = underdog_percentage / 100
        print(f"Historical underdog win rate from data: {underdog_percentage:.2f}%")
        
        for odds in underdog_odds_examples:
            payout_info = calculate_payout_american_odds(odds, bet_amount)
            implied_prob = calculate_implied_probability(odds) / 100
            
            # Expected value calculation
            expected_value = (win_rate * payout_info['profit']) - ((1 - win_rate) * bet_amount)
            
            # Break-even win rate needed
            breakeven_rate = implied_prob * 100
            
            print(f"Odds {odds:+4}: EV = ${expected_value:+7.2f} | Break-even: {breakeven_rate:.1f}% | Edge: {(win_rate - implied_prob)*100:+.1f}%")
            