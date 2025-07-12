import pandas as pd

def get_yes_no_input(prompt_message):
    """
    Prompts the user for a yes/no response and returns True for 'yes' or 'y',
    and False for 'no' or 'n'. Handles case-insensitivity and invalid input.
    """
    while True:
        user_input = input(f"{prompt_message} (y/n): ").lower().strip()
        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def run_fight_tracker():
    """
    An interactive tool to track the required upset percentage for a fight card.
    """
    # Load, sort by bout number descending, and reset the index
    draftkings = pd.read_csv("odds.csv").sort_values(by="bout_number", ascending=False).reset_index(drop=True)

    try:
        # Based on the HTML context, a common number of fights is around 13.
        # A 32% upset rate would be about 4 upsets.
        
        total_fights = len(draftkings)
        expected_upsets = int(input(f"Enter your predicted number of upsets for the card (e.g., 4): "))
    except ValueError:
        print("Invalid input. Please enter whole numbers.")
        return

    remaining_fights = total_fights
    remaining_upsets = expected_upsets
    fights_processed = 0

    print("\n--- Let's start the fight card! ---")

    while remaining_fights > 0:
        if remaining_upsets < 0:
            remaining_upsets = 0 # Can't have negative upsets

        if remaining_upsets > remaining_fights:
            print(f"\nIt's now impossible to have {expected_upsets} upsets. You need {remaining_upsets} but only {remaining_fights} fights are left.")        
        
        needed_percent = (remaining_upsets / remaining_fights) * 100
        print(f"\nFights remaining: {remaining_fights}. ")
        # print(f"Underdogs need to win {needed_percent:.1f}% of the remaining fights to hit your prediction.")
        

        # Use fights_processed for 0-based ascending indexing
        # Get the current fight's data using .iloc for efficient row access
        current_fight = draftkings.iloc[fights_processed]
        fighter_1 = current_fight['fighter_1']
        fighter_2 = current_fight['fighter_2']
        print(f"Chance of the next fight being an Underdog win {needed_percent:.1f}% ")
        print(f"\nNext Fight: {fighter_1} {current_fight['fighter_1_odds']} vs. {fighter_2} {current_fight['fighter_2_odds']}")

        if get_yes_no_input("Did this fight result in an upset?"):
            remaining_upsets -= 1
        
        fights_processed += 1
        remaining_fights -= 1

    print("\n--- Fight card finished! ---")
    if remaining_upsets == 0 and remaining_fights == 0:
        print(f"Your prediction of {expected_upsets} upsets was correct!")
    else:
        actual_upsets = expected_upsets - remaining_upsets
        print(f"The card ended with {actual_upsets} upsets, while you predicted {expected_upsets}.")

if __name__ == "__main__":
    run_fight_tracker()
