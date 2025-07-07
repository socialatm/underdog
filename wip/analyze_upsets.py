import os
from bs4 import BeautifulSoup

def analyze_upset_data(html_file_path):
    """
    Parses the underdogs.html file to calculate historical upset statistics,
    including average upsets per event and the overall upset percentage.

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

    # Find the specific H3 tag that precedes the table we want.
    h3_tag = soup.find('h3', string='MMA / UFC Betting - Favorite vs Underdog Returns over Time')
    if not h3_tag:
        print("Error: Could not find the 'Returns over Time' header in the HTML file.")
        return None

    # The table we want is the first table immediately following this H3 tag.
    data_table = h3_tag.find_next('table')
    if not data_table:
        print("Error: Could not find the data table following the header.")
        return None

    rows = data_table.find_all('tr')
    
    total_underdog_wins = 0
    event_count = 0
    total_fights = 0
    
    # Start from the second row to skip the header
    for row in rows[1:]:
        cells = row.find_all('td')
        
        # The summary row at the end has a style attribute on its cells.
        # This is a reliable way to detect the end of the data.
        if len(cells) > 2 and cells[2].get('style'):
            break
            
        # Ensure the row has enough cells to avoid an IndexError
        if len(cells) >= 4:
            try:
                # Favourite wins are in the 3rd column (index 2)
                favourite_wins = int(cells[2].text.strip())
                # Underdog wins are in the 4th column (index 3)
                underdog_wins = int(cells[3].text.strip())
                
                total_underdog_wins += underdog_wins
                total_fights += (favourite_wins + underdog_wins)
                event_count += 1
            except (ValueError, IndexError):
                # Skip any rows that are not valid event data (e.g., malformed or empty)
                continue

    if event_count == 0:
        print("No valid event data was found to perform analysis.")
        return None

    average_upsets_per_event = total_underdog_wins / event_count
    overall_upset_percentage = (total_underdog_wins / total_fights) * 100
    
    print("Successfully parsed the HTML file.")
    print("------------------------------------")
    print(f"Total events analyzed:      {event_count}")
    print(f"Total fights analyzed:      {total_fights}")
    print(f"Total underdog wins (upsets): {total_underdog_wins}")
    print(f"Average upsets per event:   {average_upsets_per_event:.2f}")
    print(f"Overall upset percentage:   {overall_upset_percentage:.2f}%")
    print("------------------------------------")
    
    return {
        "events_analyzed": event_count,
        "fights_analyzed": total_fights,
        "total_upsets": total_underdog_wins,
        "average_upsets_per_event": average_upsets_per_event,
        "overall_upset_percentage": overall_upset_percentage,
    }

if __name__ == '__main__':
    # The path to your HTML file. Please adjust this if your file is located elsewhere.
    html_file_path = r'c:\Users\raype\Documents\GitHub\underdog\underdogs.html'
    analyze_upset_data(html_file_path)