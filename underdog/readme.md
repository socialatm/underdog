# Underdog Scrapy Project

This project contains Scrapy spiders for web scraping. This `README` will guide you through setting up the project and running the spiders.

## Requirements

*   Python 3.7+
*   Scrapy

## Installation

1.  **Clone the repository (if you haven't already):**
    ```sh
    git clone <your-repo-url>
    cd underdog
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    It is a good practice to have a `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```
    If you don't have one yet, you can install Scrapy directly:
    ```sh
    pip install Scrapy
    ```

## Usage

To run a spider, use the `scrapy crawl` command from within the project's root directory (`underdog`).

```sh
py -m scrapy crawl <spider_name> -o output.json
```

## Spiders

The spiders for this project are located in the `underdog/spiders/` directory. You can add a list of your spiders here as you create them.

## Project Configuration

The main configuration for the Scrapy project can be found in `underdog/settings.py`. You can configure pipelines, middlewares, user-agent strings, and other settings in this file.

The `scrapy.cfg` file contains configuration for deploying your project with `scrapyd`.
