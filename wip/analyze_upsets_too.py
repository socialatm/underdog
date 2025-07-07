import os
from bs4 import BeautifulSoup

def _parse_returns_table(table_soup):
    """Helper function to parse the 'Returns over Time' table."""
    rows = table_soup.find_all('tr')
    
    total_underdog_wins = 0
    event_count = 0
    total_fights = 0
    
    # Start from the second row to skip the header
    for row in rows[1:]:
        cells = row.find_all('td')
        
        # The summary row at the end has a style attribute on its cells.
        if len(cells) > 2 and cells[2].get('style'):
            break
            
        if len(cells) >= 4:
            try:
                favourite_wins = int(cells[2].text.strip())
                underdog_wins = int(cells[3].text.strip())
                
                total_underdog_wins += underdog_wins
                total_fights += (favourite_wins + underdog_wins)
                event_count += 1
            except (ValueError, IndexError):
                continue

    if event_count == 0:
        return None

    return {
        "events_analyzed": event_count,
        "fights_analyzed": total_fights,
        "total_upsets": total_underdog_wins,
        "average_upsets_per_event": total_underdog_wins / event_count,
        "overall_upset_percentage": (total_underdog_wins / total_fights) * 100,
    }

def _parse_card_position_table(table_soup):
    """Helper function to parse the 'Winner Odds By Card Position' table."""
    rows = table_soup.find_all('tr')
    position_stats = []

    # Start from the second row to skip the header
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) >= 5:
            try:
                position = cells[0].text.strip()
                fav_wins = int(cells[2].text.strip())
                dog_wins = int(cells[4].text.strip())
                total_bouts = fav_wins + dog_wins
                upset_percent = (dog_wins / total_bouts) * 100 if total_bouts > 0 else 0
                position_stats.append({"position": position, "upset_percentage": upset_percent})
            except (ValueError, IndexError):
                continue
    return position_stats

def analyze_upset_data(html_file_path):
    """
    Parses the underdogs.html file to calculate historical upset statistics,
    including overall returns and breakdown by card position.

    Args:
        html_file_path (str): The full path to the underdogs.html file.

    Returns:
        dict: A dictionary containing the calculated statistics, or None if an
              error occurs.
    """
    if not os.path.exists(html_file_path):
        print(f"Error: File not found at {html_file_path}")
        return None

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    soup = BeautifulSoup(content, 'html.parser')

    # --- 1. Parse the overall returns table ---
    returns_h3 = soup.find('h3', string='MMA / UFC Betting - Favorite vs Underdog Returns over Time')
    if not returns_h3:
        print("Error: Could not find the 'Returns over Time' header in the HTML file.")
        return None
    
    returns_table = returns_h3.find_next('table')
    if not returns_table:
        print("Error: Could not find the 'Returns over Time' data table.")
        return None
    
    overall_stats = _parse_returns_table(returns_table)
    if not overall_stats:
        print("No valid event data was found in the 'Returns over Time' table.")
        return None
    
    # --- 2. Parse the card position table ---
    position_h3 = soup.find('h3', string=lambda t: t and 'Winner Odds By Card Position' in t)
    if not position_h3:
        print("Warning: Could not find the 'Winner Odds By Card Position' header.")
        card_position_stats = []
    else:
        position_table = position_h3.find_next('table')
        if not position_table:
            print("Warning: Could not find the 'Winner Odds By Card Position' data table.")
            card_position_stats = []
        else:
            card_position_stats = _parse_card_position_table(position_table)
    
    # --- 3. Print results and return data ---
    print("Successfully parsed the HTML file.")
    print("\n--- Overall Historical Analysis ---")
    print(f"Total events analyzed:      {overall_stats['events_analyzed']}")
    print(f"Total fights analyzed:      {overall_stats['fights_analyzed']}")
    print(f"Total underdog wins (upsets): {overall_stats['total_upsets']}")
    print(f"Average upsets per event:   {overall_stats['average_upsets_per_event']:.2f}")
    print(f"Overall upset percentage:   {overall_stats['overall_upset_percentage']:.2f}%")
    
    if card_position_stats:
        print("\n--- Upset Percentage by Card Position ---")
        for stat in card_position_stats:
            print(f"{stat['position']:<12}: {stat['upset_percentage']:.2f}%")
    
    final_data = overall_stats
    final_data["card_position_stats"] = card_position_stats
    return final_data


if __name__ == '__main__':
    # The path to your HTML file. Please adjust this if your file is located elsewhere.
    html_file_path = r'c:\Users\raype\Documents\GitHub\underdog\underdogs.html'
    analyze_upset_data(html_file_path)
    