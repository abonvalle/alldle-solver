import numpy as np
import pandas as pd
from collections import defaultdict
from constants import AVAILABLE_GAMES
from custom_types import GamePropertyClass, GameClass
from bcolors import bcolors
from typing import  Literal
import argparse

def compute_elimination_score(data, test_guess, properties: list[GamePropertyClass]):
    """
    Calculates how many characters each test_guess would eliminate
    based on the feedback it would generate against all other characters.
    """
    feedback_patterns = defaultdict(int)

    for _, target in data.iterrows():
        if (test_guess == target).all():
            continue  # Skip if comparing with itself

        feedback = [] 
        for col in properties:
            guess_value = test_guess[col["name"]]
            target_value = target[col["name"]]

            if col["type"] == "range":
                if guess_value == target_value:
                    feedback.append("G")
                elif guess_value < target_value:
                    feedback.append("H")  # Guess is lower → actual is greater
                else:
                    feedback.append("L")  # Guess is greater → actual is lower
                    
            elif col["type"] == "exact":
                if guess_value == target_value:
                    feedback.append("G")
                elif guess_value & target_value:  # Overlapping sets
                    feedback.append("O")
                else:
                    feedback.append("R")

        feedback_tuple = tuple(feedback)
        feedback_patterns[feedback_tuple] += 1

    # The score is how many candidates are eliminated on average
    total_tests = len(data) - 1  # Exclude itself
    avg_elimination = sum(total_tests - count for count in feedback_patterns.values()) / total_tests

    return avg_elimination

def get_best_guess(data, properties: list[GamePropertyClass]):
    """
    Selects the best first guess by evaluating which character 
    has the highest elimination potential.
    """
    if data.empty:
        print("No candidates available!")
        return None

    best_guess = None
    best_score = -1

    for index, row in data.iterrows():
        score = compute_elimination_score(data, row, properties)
        # print(score, row.values[0])
        if score > best_score:
            best_score = score
            best_guess = row

    # print(f"Best initial guess chosen with elimination score: {best_score:.2f}")
    return best_guess

# Function to filter candidates based on feedback
def filter_candidates(data, guess, feedback, properties):
    """
    - 'G' (True): Keep only exact matches.
    - 'R' (False): Remove characters with any overlapping values.
    - 'O' (Partial): Keep characters with at least some overlap, but not exact matches.
    - 'L' (Lower) / 'H' (Higher): Only for Ranges property, filter accordingly.
    """
    mask = np.ones(len(data), dtype=bool)
    # print(guess)
    # for i, fb in enumerate(feedback):
    for i, col in enumerate(properties):
        guess_value = guess[col["name"]]  # Offset to match column index
        if col["type"] == "range":  # Special handling for Year
            if feedback[i] == "G":
                mask &= data[col["name"]] == guess_value
            elif feedback[i] == "L":
                mask &= data[col["name"]] < guess_value
            elif feedback[i] == "H":
                mask &= data[col["name"]] > guess_value
        
        elif col["type"] == "exact":  # Normal filtering for other properties
            if feedback[i] == "G":
                mask &= data[col["name"]] == guess_value  # Exact match required
            elif feedback[i] == "R":
                mask &= ~data[col["name"]].apply(lambda x: bool(x & guess_value))  # No overlap
            elif feedback[i] == "O":
                mask &= data[col["name"]].apply(lambda x: bool(x & guess_value) and x != guess_value)  # Some overlap, but not exact
            
    return data[mask]

def start_game(selected_game:GameClass,first_guess:str):
    print(f"Starting {selected_game['name']} Solver...")
    # Load character database
    df:pd.DataFrame = pd.read_csv(selected_game["dataPath"])
    alldle_solver(selected_game,df,first_guess)
    
def start_solver(game_name:GameClass["name"], first_guess:str):
    selected_game = False
    if(game_name):
        selected_game = next((game for game in AVAILABLE_GAMES if game["name"] == game_name), None)
        if selected_game:
            start_game(selected_game,first_guess)
        else:
            print("Invalid game name. Please enter a valid game.")
            
    # Display the available games
    options = "\n".join(f"{game['id']} - {game['name']}" for game in AVAILABLE_GAMES)

    # Convert user input to integer
    while selected_game==False:
        try:
            user_choice = input(f"Select a game by number:\n{options}\n> ")
            user_choice = int(user_choice)
            selected_game = next((game for game in AVAILABLE_GAMES if game["id"] == user_choice), None)

            if selected_game != False:
                return start_game(selected_game,first_guess)
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def set_alldle_parameters(properties:list[GamePropertyClass], df:pd.DataFrame):
    # Convert categorical data into sets (for handling partial matches)
    for col in df.columns:
        property:GamePropertyClass = next((el for el in properties if el["name"] == col), None)
        if property == None:
            df.drop(col, axis=1, inplace=True)
            continue
        if property["type"] == "exact":
            df[col] = df[col].astype(str).apply(lambda x: set(x.split(";")))
        elif property["type"] == "range":
            df[col] = df[col].astype(int)
    return df

def property_to_accepted_feedback(propertyType:Literal["guess", "exact", "range"]):
    match propertyType:
        case "guess":
            return []
        case "exact":
            return ["G","R","O"]
        case "range":
            return ["G","H","L"]
        case _:
            return []
        
def print_invalid_feedback(properties:list[GamePropertyClass]):
    print(f"{bcolors.WARNING}Invalid feedback!{bcolors.ENDC}")
    options = "\n".join(f"{property['name']} - {', '.join(property_to_accepted_feedback(property['type']))}" for property in properties[1:])
    print(f"Feedback should be {len(properties[1:])} chars long and match the following properties in the right order:\n{options}\n> ")

   
# Main game loop
def alldle_solver(selected_game:GameClass, df:pd.DataFrame, first_guess:str):
    df = set_alldle_parameters(selected_game["properties"], df)
    properties = [prop for prop in selected_game["properties"] if prop["type"] != "guess"]

    # First move
    best_guess = get_best_guess(df,properties)
    print(f"Best initial guess: {bcolors.WARNING}{bcolors.BOLD}{best_guess.values[0]}{bcolors.ENDC}")
    
    remaining_candidates = df.copy()
    
    while len(remaining_candidates) > 1:
        # Get user feedback
        feedback = input(f"Enter feedback for each property ({bcolors.BOLD}{bcolors.OKGREEN}G{bcolors.ENDC}=Correct, {bcolors.BOLD}{bcolors.FAIL}R{bcolors.ENDC}=Wrong (not for ranges), {bcolors.BOLD}{bcolors.WARNING}O{bcolors.ENDC}=Partial (not for ranges), {bcolors.BOLD}{bcolors.HEADER}L{bcolors.ENDC}=Lower (only for ranges), {bcolors.BOLD}{bcolors.HEADER}H{bcolors.ENDC}=Higher (only for ranges)): \n").strip().upper()
        if len(feedback) != len(properties) or any(f not in property_to_accepted_feedback(properties[idx]["type"]) for idx,f in enumerate(feedback)):
            print_invalid_feedback(properties)
            continue

        # Filter remaining candidates
        remaining_candidates = filter_candidates(remaining_candidates, best_guess, feedback, properties)
        
        if remaining_candidates.empty:
            print(f"{bcolors.BOLD}{bcolors.FAIL}No valid candidates left! Please check the feedback entered.{bcolors.ENDC}")
            break
        elif len(remaining_candidates) == 1:
            print(f"\nThe character is: {bcolors.OKGREEN}{bcolors.BOLD}{remaining_candidates.iloc[0].values[0]}{bcolors.ENDC}\n\n")
            break
        else:
            best_guess = get_best_guess(remaining_candidates,properties)
            print(f"Next best guess: {bcolors.WARNING}{bcolors.BOLD}{best_guess.values[0]}{bcolors.ENDC}")
            print(f"Remaining candidates: {bcolors.OKCYAN}{bcolors.BOLD}{', '.join(remaining_candidates.iloc[:, 0].astype(str))}{bcolors.ENDC}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the app with the game of your choice")
    parser.add_argument("--game","-g", type=str, help="The game to start the app with")
    parser.add_argument("--start_with", "-s", type=str, help="The first guess to start the game with")

    args = parser.parse_args()
    start_solver(args.game,args.start_with)