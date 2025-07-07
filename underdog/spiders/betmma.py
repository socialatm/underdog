from pathlib import Path
import scrapy
import re
from datetime import datetime
import dateutil.parser


class Betmma(scrapy.Spider):
    name = "betmma"
    allowed_domains = ["betmma.tips"]
    start_urls = ["https://www.betmma.tips/mma_betting_favorites_vs_underdogs.php?Org=1"]

    def extract_formatted_date(self, text):
        """Extract and convert date/time text to 'Dec 25 2023' format"""
        if not text or not text.strip():
            return '""'
        
        # Clean the text - remove extra whitespace and common non-date characters
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove any link information if present
        if " | Links:" in cleaned_text:
            cleaned_text = cleaned_text.split(" | Links:")[0].strip()
        
        try:
            # Try to parse the date using dateutil (handles many formats)
            parsed_date = dateutil.parser.parse(cleaned_text, fuzzy=True)
            # Format as "Dec 25 2023"
            formatted_date = parsed_date.strftime("%b %d %Y")
            return f'"{formatted_date}"'
        except (ValueError, TypeError, dateutil.parser.ParserError):
            # If parsing fails, try some common patterns manually
            date_patterns = [
                r'(\d{1,2})/(\d{1,2})/(\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
                r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
                r'(\d{1,2})-(\d{1,2})-(\d{4})',  # MM-DD-YYYY or DD-MM-YYYY
                r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', # Month DD, YYYY
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, cleaned_text)
                if match:
                    try:
                        if pattern == date_patterns[0]:  # MM/DD/YYYY format
                            month, day, year = match.groups()
                            date_obj = datetime(int(year), int(month), int(day))
                        elif pattern == date_patterns[1]:  # YYYY-MM-DD format
                            year, month, day = match.groups()
                            date_obj = datetime(int(year), int(month), int(day))
                        elif pattern == date_patterns[2]:  # MM-DD-YYYY format
                            month, day, year = match.groups()
                            date_obj = datetime(int(year), int(month), int(day))
                        elif pattern == date_patterns[3]:  # Month DD, YYYY format
                            month_name, day, year = match.groups()
                            date_obj = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y")
                        
                        # Format as "Dec 25 2023"
                        formatted_date = date_obj.strftime("%b %d %Y")
                        return f'"{formatted_date}"'
                    except (ValueError, TypeError):
                        continue
        
        # If no date pattern found, return original text in quotes
        return f'"{text.strip()}"'

    def extract_number(self, text):
        """Extract numeric value from text string"""
        if not text or not text.strip():
            return ""
        
        # Remove common non-numeric characters but keep +, -, and decimal points
        # This handles cases like "$100", "50%", "+150", "-200", "1,500", etc.
        cleaned = re.sub(r'[^\d+\-.,]', '', text.strip())
        
        # Handle empty string after cleaning
        if not cleaned:
            return ""
        
        # Try to extract a number (handles +/- signs, decimals, commas)
        number_match = re.search(r'[+\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?', cleaned)
        if number_match:
            number_str = number_match.group().replace(',', '')
            try:
                # Try to convert to int first, then float if needed
                if '.' in number_str:
                    return str(float(number_str))
                else:
                    return str(int(number_str))
            except ValueError:
                pass
        
        # If no number found, return original text in quotes
        return f'"{text.strip()}"'

    def parse(self, response):
        # Extract table with 98% width
        table = response.css('table[width="98%"]').get()
        
        if table:
               
            # Extract table data including links - FIRST 4 CELLS ONLY
            table_rows = response.css('table[width="98%"] tr')
            table_data = []
            
            for row in table_rows:
                cells = row.css('td, th')[:4]  # Limit to first 4 cells
                row_data = []
                
                for cell in cells:
                    # Get all text content including text inside links
                    all_text = cell.css('::text').getall()
                    # Get link text specifically
                    link_text = cell.css('a::text').getall()
                    # Get link URLs
                    link_urls = cell.css('a::attr(href)').getall()
                    
                    # Combine all text content
                    cell_text = ' '.join([text.strip() for text in all_text if text.strip()])
                    
                    # If there are links, add URL information
                    if link_urls:
                        link_info = []
                        for i, url in enumerate(link_urls):
                            link_text_for_url = link_text[i] if i < len(link_text) else "Link"
                            # Make URL absolute if it's relative
                            absolute_url = response.urljoin(url)
                            link_info.append(f"{link_text_for_url} ({absolute_url})")
                        
                        # Add link information to cell text
                        if cell_text and link_info:
                            cell_text += " | Links: " + " | ".join(link_info)
                        elif link_info:
                            cell_text = "Links: " + " | ".join(link_info)
                    
                    row_data.append(cell_text)
                
                # Only add rows that have at least one cell with content
                if row_data and any(cell.strip() for cell in row_data):
                    # Pad with empty strings if less than 4 cells
                    while len(row_data) < 4:
                        row_data.append("")
                    table_data.append(row_data)  # Keep as list for easier processing
            
            if table_data:
                
                # Create CSV version with header row handling and first cell filtering
                csv_filename = "table_98_percent_first4.csv"
                csv_data = []
                
                for row_index, row in enumerate(table_data):
                    # Check if this is the first row (header row) - always include it
                    is_header_row = row_index == 0
                    
                    # For data rows, check if first cell is not empty
                    first_cell_has_content = row[0] and row[0].strip()
                    
                    # Only process row if it's a header row OR if first cell has content
                    if is_header_row or first_cell_has_content:
                        csv_row = []
                        
                        for i, field in enumerate(row):
                            if is_header_row:
                                # For header row, just quote all fields as strings
                                escaped_field = field.replace('"', '""')
                                csv_row.append(f'"{escaped_field}"')
                            else:
                                # For data rows, apply conversions
                                if i == 0:  # First column - convert to "Dec 25 2023" format
                                    formatted_date = self.extract_formatted_date(field)
                                    csv_row.append(formatted_date)
                                elif i >= 2:  # Last 2 columns (index 2 and 3) - convert to numbers
                                    numeric_value = self.extract_number(field)
                                    csv_row.append(numeric_value)
                                else:  # Second column - keep as quoted string
                                    escaped_field = field.replace('"', '""')
                                    csv_row.append(f'"{escaped_field}"')
                        
                        csv_data.append(','.join(csv_row))
                
                Path(csv_filename).write_text('\n'.join(csv_data), encoding='utf-8')
                self.log(f"Saved CSV with {len(csv_data)} rows (including header) - filtered by non-empty first cell")
                print(f"Saved CSV with {len(csv_data)} rows (including header) - filtered by non-empty first cell")
        else:
            self.log("No table with 98% width found")
            print("No table with 98% width found")
        
        # Also save the full page for reference
        filename = f"underdogs.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved full page to {filename}")
        print(f"Saved full page to {filename}")
        