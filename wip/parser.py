import pandas as pd
from bs4 import BeautifulSoup

def get_card_position_df(html_content: str) -> pd.DataFrame | None:
    """
    Parses the HTML content to find the 'Winner Odds By Card Position' table
    and returns it as a pandas DataFrame.

    Args:
        html_content: The HTML content of the page as a string.

    Returns:
        A pandas DataFrame containing the card position data, or None if not found.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the h3 tag for "Winner Odds By Card Position"
    position_h3 = soup.find('h3', string=lambda t: t and 'Winner Odds By Card Position' in t)

    if not position_h3:
        print("Could not find the 'Winner Odds By Card Position' section.")
        return None

    # The h3 is in a td, in a tr. The table is in the next tr's td.
    table = position_h3.find_parent('tr').find_next_sibling('tr').find('table')

    if not table:
        print("Could not find the table for card positions.")
        return None

    # Use pandas to read the HTML table. It returns a list of DataFrames.
    df = pd.read_html(str(table), flavor='bs4')[0]

    # The original header has two columns named '%'. Let's rename them for clarity.
    df.columns = [
        'Position', 'Fights', 'Fav Wins', 'Fav Wins %', 'Dog Wins', 'Dog Wins %',
        'Avg Odds (Winner)', 'Fav | Dog', '$10 on all Favs', '$10 on all Dogs'
    ]

    # The 'Fav | Dog' column contains HTML for a progress bar, which isn't useful data.
    df = df.drop(columns=['Fav | Dog'])

    return df

if __name__ == '__main__':
    # Provide the path to your HTML file
    file_path = r'c:\Users\raype\Documents\GitHub\underdog\underdogs.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    card_position_df = get_card_position_df(html)

    print(card_position_df.head())

    if card_position_df is not None:
        print("Successfully extracted the 'Winner Odds By Card Position' table:")
        print(card_position_df.to_string())

