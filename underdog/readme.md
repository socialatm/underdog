# BetMMA Scraper

This is a Scrapy project designed to scrape MMA event data from [betmma.tips](https://www.betmma.tips/). It specifically targets the page listing historical data on favorite vs. underdog wins for UFC events.

The primary spider, `betmma`, extracts event details and saves them to a CSV file.

## Features

- Scrapes event date, name, and URL.
- Extracts the number of wins for favorites and underdogs for each event.
- Cleans and formats data (dates to `YYYY-MM-DD`, numbers to integers).
- Saves the output to `betmma.csv`.

## Requirements

- Python 3.8+
- Scrapy
- python-dateutil

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd underdog
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install scrapy python-dateutil
    ```

## Usage

To run the spider, navigate to the project's root directory (`underdog/`) and execute the following command:

```bash
scrapy crawl betmma
```

This command will start the crawl and, upon completion, create a `betmma.csv` file in the same directory. The spider is configured to overwrite this file on each run.

## Output

The scraper will produce a `betmma.csv` file with the following columns:

- `date`: The date of the event in `YYYY-MM-DD` format.
- `event`: The name of the MMA event.
- `event_url`: The full URL to the event details page on `betmma.tips`.
- `favourite_wins`: The number of fights won by the betting favorite.
- `underdog_wins`: The number of fights won by the betting underdog.

### Example Output (`betmma.csv`)

```csv
date,event,event_url,favourite_wins,underdog_wins
2024-02-17,UFC 298: Volkanovski vs. Topuria,https://www.betmma.tips/event_fights.php?EID=1103,6,5
2024-02-10,UFC Fight Night: Hermansson vs. Pyfer,https://www.betmma.tips/event_fights.php?EID=1107,8,5
2024-02-03,UFC Fight Night: Dolidze vs. Imavov,https://www.betmma.tips/event_fights.php?EID=1106,6,6
2024-01-20,UFC 297: Strickland vs. Du Plessis,https://www.betmma.tips/event_fights.php?EID=1102,8,4
...
```

---

*This project uses Scrapy. For more information, visit the Scrapy documentation.*