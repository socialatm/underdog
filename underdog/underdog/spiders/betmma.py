import scrapy
import re
import dateutil.parser


class BetmmaSpider(scrapy.Spider):
    name = "betmma"
    allowed_domains = ["betmma.tips"]
    start_urls = ["https://www.betmma.tips/mma_betting_favorites_vs_underdogs.php?Org=1"]

    custom_settings = {
        "FEEDS": {
            "betmma.csv": {"format": "csv", "overwrite": True, "encoding": "utf-8"},
        },
    }

    def extract_formatted_date(self, text):
        """Extract and convert date/time text to 'YYYY-MM-DD' format."""
        if not text or not text.strip():
            return None

        try:
            # dateutil is powerful and can parse many date formats
            parsed_date = dateutil.parser.parse(text.strip())
            # ISO format YYYY-MM-DD is standard and sorts well
            return parsed_date.strftime("%Y-%m-%d")
        except (ValueError, TypeError, dateutil.parser.ParserError):
            self.log(f"Could not parse date: {text.strip()}", level=scrapy.log.WARNING)
            return None

    def extract_number(self, text):
        """Extract an integer or float value from a text string."""
        if not text or not text.strip():
            return None

        number_match = re.search(r'[+\-]?\d{1,3}(?:,\d{3})*(?:\.\d+)?', text.strip())
        if number_match:
            number_str = number_match.group().replace(',', '')
            try:
                if '.' in number_str:
                    return float(number_str)
                else:
                    return int(number_str)
            except ValueError:
                self.log(f"Could not convert to number: {number_str}", level=scrapy.log.WARNING)

        self.log(f"No number found in: {text.strip()}", level=scrapy.log.WARNING)
        return None

    def parse(self, response):
        """
        This method parses the response and yields structured data for each table row.
        Scrapy's feed exporters can then be used to save this data to CSV, JSON, etc.
        Example: scrapy crawl betmma -o output.csv
        """
        self.log(f"Parsing page: {response.url}")
        table_rows = response.css('table[width="98%"] tr')

        # Skip header row (the first `tr`) and process the rest
        for row in table_rows[1:]:
            cells = row.css('td')

            # Skip rows that don't have enough cells or are summary rows (empty first cell)
            if len(cells) < 4 or not cells[0].css('::text').get('').strip():
                continue

            # Extract data from the first 4 cells
            date_raw = cells[0].css('::text').get()
            event_text = cells[1].css('a::text').get()
            event_url = cells[1].css('a::attr(href)').get()
            fav_wins_raw = cells[2].css('::text').get()
            underdog_wins_raw = cells[3].css('::text').get()

            yield {
                'date': self.extract_formatted_date(date_raw),
                'event': event_text.strip() if event_text else None,
                'event_url': response.urljoin(event_url) if event_url else None,
                'favourite_wins': self.extract_number(fav_wins_raw),
                'underdog_wins': self.extract_number(underdog_wins_raw),
            }