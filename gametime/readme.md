# GameTime - Fight Upset Tracker

`GameTime` is a simple, interactive command-line tool designed for fight fans. It helps you track the required upset percentage for a fight card based on your initial prediction. As each fight concludes, you tell the tool whether it was an upset, and it dynamically recalculates what's needed from the remaining fights to meet your goal.

## Features

- **Interactive CLI**: Guides you through a fight card, one bout at a time.
- **Dynamic Calculations**: Calculates the required upset percentage in real-time as the card progresses.
- **Live-Ready**: Reloads fight data before each bout, allowing for live updates to odds if the source file changes during the event.
- **Final Summary**: Provides a summary at the end of the card comparing your prediction to the actual outcome.

## Requirements

- Python 3.6+
- `pandas` library

## Setup

1.  Ensure you have Python installed on your system.
2.  Install the required `pandas` library:
    ```bash
    pip install pandas
    ```
3.  Create an `odds.csv` file in the same directory as the `gametime.py` script. See the format requirements below.

## `odds.csv` File Format

The script requires a CSV file named `odds.csv` to be present in the same directory. The file must contain a header and the following columns:

- `bout_number`: An integer to define the order of the fights (e.g., 1 for the first fight, 2 for the second). The script processes fights in ascending order of this number.
- `fighter_1`: Name of the first fighter (string).
- `fighter_1_odds`: Odds for the first fighter (e.g., `+150`, `-200`).
- `fighter_2`: Name of the second fighter (string).
- `fighter_2_odds`: Odds for the second fighter.

**Example `odds.csv`:**
```csv
bout_number,fighter_1,fighter_1_odds,fighter_2,fighter_2_odds
1,"John Doe",-110,"Jane Smith",-110
2,"Peter Jones",+250,"Mark Rivera",-300
3,"Alex Costa",-500,"Chris Lee",+400
```

## Usage

1.  Navigate to the script's directory in your terminal.
2.  Run the script:
    ```bash
    python gametime.py
    ```
3.  The script will first ask for your predicted number of upsets for the entire card.
    ```
    Enter your predicted number of upsets for the card (e.g., 4): 4
    ```
4.  For each fight, it will display the details and ask if the result was an upset. Respond with `y` for yes or `n` for no.
    ```
    --- Let's start the fight card! ---

    Fights remaining: 13.
    Chance of the next fight being an Underdog win 30.8%

    Next Fight: Fighter A -150 vs. Fighter B +125
    Did this fight result in an upset? (y/n): y
    ```
5.  The tool will continue until all fights are processed and then display a final summary of your prediction's accuracy.
