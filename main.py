import pandas as pd
import os

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
        #print(f"DataFrame shape: {df.shape}")
        #print(f"Columns: {list(df.columns)}")
        #print("\nFirst few rows:")
        #print(df.head())
        
        # Display data types
        #print("\nData types:")
        #print(df.dtypes)
        
        # Display basic statistics for numeric columns
        # if df.select_dtypes(include=['number']).shape[1] > 0:
            # print("\nBasic statistics:")
            # print(df.describe())
        
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
        
        # events with 4 underdog wins
        #four_underdog_wins = dataframe[dataframe['Underdog Wins'] == 4]
        #print(f"\nNumber of events with 4 underdog wins: {len(four_underdog_wins)}")

        #percent of events with 4 underdog wins
        #percent_four_underdog_wins = (len(four_underdog_wins) / total_events) * 100
        #print(f"Percentage of events with 4 underdog wins: {percent_four_underdog_wins:.2f}%")

        # minimum number of underdog wins
        min_underdog_wins = dataframe['Underdog Wins'].min()
        print(f"\nMinimum number of underdog wins: {min_underdog_wins}")
        #min_underdog_wins = 4  # Set minimum underdog wins to 3 for further calculations

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
            #print(f"Number of events with {i} underdog wins: {count}")
            # calculate the percentage of events with i underdog wins
            percent_i_underdog_wins = (count / events_gte_min) * 100
            print(f"Percentage of events with {i} underdog wins: {percent_i_underdog_wins:.2f}%")
            #print(f"\n")
        
