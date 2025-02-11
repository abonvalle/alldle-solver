import numpy as np
import pandas as pd
from collections import defaultdict
from constants import AVAILABLE_GAMES, FEEDBACKS
from custom_types import GamePropertyClass, GameClass
from bcolors import bcolors
from typing import  Literal
import argparse

global VERBOSE
global FAST_GAME
global GAME

def compute_elimination_score(data, test_guess, properties: list[GamePropertyClass], guess_property_name: str):
    """
    Calculates how many characters each test_guess would eliminate
    based on the feedback it would generate against all other characters.
    """
    feedback_patterns = defaultdict(int)
    for _, target in data.iterrows():
        if (test_guess[guess_property_name] == target[guess_property_name]):
            continue  # Skip if comparing with itself
        
        feedback = [] 
        for col in properties:
            guess_value = test_guess[col["name"]]
            target_value = target[col["name"]]

            if col["type"] == "range":
                if guess_value == target_value:
                    feedback.append(FEEDBACKS["correct"]["letter"])
                elif guess_value < target_value:
                    feedback.append(FEEDBACKS["greater"]["letter"])  # Guess is lower → actual is greater
                else:
                    feedback.append(FEEDBACKS["lower"]["letter"])  # Guess is greater → actual is lower
                    
            elif col["type"] == "exact":
                if guess_value == target_value:
                    feedback.append(FEEDBACKS["correct"]["letter"])
                elif guess_value & target_value:  # Overlapping sets
                    feedback.append(FEEDBACKS["partial"]["letter"])
                else:
                    feedback.append(FEEDBACKS["incorrect"]["letter"])

        feedback_tuple = tuple(feedback)
        feedback_patterns[feedback_tuple] += 1

    # The score is how many candidates are eliminated on average
    total_tests = len(data) - 1  # Exclude itself
    avg_elimination = sum(total_tests - count for count in feedback_patterns.values()) / total_tests

    return avg_elimination

def compute_every_elimination_score(data, properties: list[GamePropertyClass], guess_property_name: str):
    if data.empty:
        print("No candidates available!")
        return None

    data["elimination_score"] = data.apply(lambda row: compute_elimination_score(data, row, properties, guess_property_name), axis=1)
    return data

# Function to filter candidates based on feedback
def filter_candidates(data, guess, feedback, properties):
    mask = np.ones(len(data), dtype=bool)

    for i, col in enumerate(properties):
        guess_value = guess[col["name"]] 
        if col["type"] == "range":  # Special handling for Ranges property
            if feedback[i] == FEEDBACKS["correct"]["letter"]:
                mask &= data[col["name"]] == guess_value
            elif feedback[i] == FEEDBACKS["lower"]["letter"]:
                mask &= data[col["name"]] < guess_value
            elif feedback[i] == FEEDBACKS["greater"]["letter"]:
                mask &= data[col["name"]] > guess_value
        
        elif col["type"] == "exact":  # Normal filtering for other properties
            if feedback[i] == FEEDBACKS["correct"]["letter"]:
                mask &= data[col["name"]] == guess_value  # Exact match required
            elif feedback[i] == FEEDBACKS["incorrect"]["letter"]:
                mask &= ~data[col["name"]].apply(lambda x: bool(x & guess_value))  # No overlap
            elif feedback[i] == FEEDBACKS["partial"]["letter"]:
                mask &= data[col["name"]].apply(lambda x: bool(x & guess_value) and x != guess_value)  # Some overlap, but not exact
            
    return data[mask]

def start_game(first_guess:str):
    print(f"Starting {GAME['name']} Solver...")
    # Load character database
    df:pd.DataFrame = pd.read_csv(GAME["dataPath"])
    alldle_solver(GAME,df,first_guess)
    
def start_solver(first_guess:str):
    global GAME
    if GAME == "ERROR":
        print("Invalid game name. Please enter a valid game.")
            
    # Display the available games
    options = "\n".join(f"{game['id']} - {game['name']}" for game in AVAILABLE_GAMES)

    # Convert user input to integer
    while GAME == "ERROR" or GAME == None:
        try:
            user_choice = input(f"Select a game by number:\n{options}\n> ")
            user_choice = int(user_choice)
            GAME = next((game for game in AVAILABLE_GAMES if game["id"] == user_choice), None)

            if GAME == None:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    start_game(first_guess)

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
            return [FEEDBACKS["correct"]["letter"],FEEDBACKS["incorrect"]["letter"],FEEDBACKS["partial"]["letter"]]
        case "range":
            return [FEEDBACKS["correct"]["letter"],FEEDBACKS["greater"]["letter"],FEEDBACKS["lower"]["letter"]]
        case _:
            return []
        
def print_invalid_feedback(properties:list[GamePropertyClass]):
    print(f"{bcolors.WARNING}Invalid feedback!{bcolors.ENDC}")
    if VERBOSE:
        options = "\n".join(f"{property['name']} - {', '.join(property_to_accepted_feedback(property['type']))}" for property in properties)
        print(f"Feedback should be {len(properties[1:])} chars long and match the following properties in the right order:\n{options}\n> ")

def print_remaining_candidates(remaining_candidates:pd.DataFrame,guess_property_name:str):
    if VERBOSE:
        candidates = ", ".join(
            f"{bcolors.OKCYAN}{bcolors.BOLD}{row[guess_property_name]}{bcolors.ENDC} (x̄ = {int(row['elimination_score'])})"
            for _, row in remaining_candidates.iterrows()
        )
        print(f"Remaining candidates: {candidates}")
  
def print_best_guess(best_guess:pd.Series,guess_property_name:str):
    print(f"Best guess: {bcolors.WARNING}{bcolors.BOLD}{best_guess[guess_property_name]}{bcolors.ENDC} (x̄ = {int(best_guess["elimination_score"])})")
     
  
def print_result(result:str):
    print(f"\nThe character is: {bcolors.OKGREEN}{bcolors.BOLD}{result}{bcolors.ENDC}\n\n")
    
def get_user_feedback(properties:list[GamePropertyClass]):
    feedback = None
    while feedback == None:
        if VERBOSE:
            inputTxt = f"Enter feedback for each property ({FEEDBACKS["correct"]["label"]}={FEEDBACKS["correct"]["description"]}, {FEEDBACKS["incorrect"]["label"]}={FEEDBACKS["incorrect"]["description"]} (not for ranges), {FEEDBACKS["partial"]["label"]}={FEEDBACKS["partial"]["description"]} (not for ranges), {FEEDBACKS["lower"]["label"]}={FEEDBACKS["lower"]["description"]} (only for ranges), {FEEDBACKS["greater"]["label"]}={FEEDBACKS["greater"]["description"]} (only for ranges)): \n"
        else:
            feedbacks=  "|".join(f["label"] for f in FEEDBACKS.values())
            inputTxt = f"Enter feedback ({feedbacks})\n"
        feedback = input(inputTxt).strip().upper()
        if len(feedback) != len(properties) or any(f not in property_to_accepted_feedback(properties[idx]["type"]) for idx,f in enumerate(feedback)):
            print_invalid_feedback(properties)
            feedback = None
            continue 
    return feedback 
   
# Main game loop
def alldle_solver(selected_game:GameClass, df:pd.DataFrame, first_guess:str):
    df = set_alldle_parameters(selected_game["properties"], df)
    properties = [prop for prop in selected_game["properties"] if prop["type"] != "guess"]
    guess_property_name = next((prop for prop in selected_game["properties"] if prop["type"] == "guess"), None)["name"]
    remaining_candidates = df.copy()
    
    while len(remaining_candidates) > 1:
 
        remaining_candidates = compute_every_elimination_score(remaining_candidates,properties,guess_property_name)
        best_guess = remaining_candidates.loc[remaining_candidates["elimination_score"].idxmax()]
        print_remaining_candidates(remaining_candidates,guess_property_name)
        print_best_guess(best_guess,guess_property_name)
        
        # Get user feedback
        feedback = get_user_feedback(properties)
          
        # Filter remaining candidates
        remaining_candidates = filter_candidates(remaining_candidates, best_guess, feedback, properties)
               
    if remaining_candidates.empty:
        print(f"{bcolors.BOLD}{bcolors.FAIL}No valid candidates left! Please check the feedback entered.{bcolors.ENDC}")
    else:
        print_result(remaining_candidates[guess_property_name].values[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the app with the game of your choice")
    parser.add_argument("--game","-g", type=str,default=None, help="The game to start the app with")
    parser.add_argument("--start_with", "-s", type=str, help="The first guess to start the game with")
    parser.add_argument("--fast_game", "-f", action='store_true', help="Whether the game should be played in fast mode (feedback only)")
    parser.add_argument("--quiet", "-q", action='store_true',default=False, help="Whether the script should be verbose or not")
    args = parser.parse_args()
    VERBOSE = not args.quiet
    FAST_GAME = args.fast_game
    GAME = next((game for game in AVAILABLE_GAMES if game["name"] == args.game), "ERROR") if args.game != None else None
    
    start_solver(args.start_with)