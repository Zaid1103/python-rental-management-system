
"""
F311024 December 2023
This program manages the game return process, including checking return status, updating return dates, and collecting user feedback.

Functions:
1. `gameID_to_return_prompt()`: Prompts the user to enter the game ID of the game they wish to return.
   

2. `already_returned(game_id)`: Checks if the game with the given ID has already been returned by reading the rental history.
  

3. `return_game2(game_id, return_date)`: Returns the game by updating the return date in the rental history.
   

4. `give_feedback(game_id, rating, comment)`: Prompts the user to give feedback on a game, including a rating and comment.


5. `main()`: The main function that orchestrates the game return process.
   Gets user input, checks if the game has already been returned, returns the game, and asks for feedback.
"""

import database
import csv
import subscriptionManager
import gamesearch
import feedbackManager

# Function to prompt the user to enter the game ID of the game they wish to return
def gameID_to_return_prompt():
    """
    Prompts the user to enter the game ID of the game they wish to return and returns the entered game ID.

    Returns:
    - str: The entered game ID.
    """
    gameID = input("Please enter game ID of the game you wish to return")
    return gameID

# Function to check if the game with the given ID has already been returned
def already_returned(game_id):
    """
    Checks if the game with the given ID has already been returned by reading the rental history.

    Parameters:
    - game_id (str): The ID of the game to check for return status.

    Returns:
    - bool: True if the game has already been returned, False otherwise.
    """
    with open('rental.txt', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        header = reader.fieldnames

    # Determine if the game has already been returned
    already_returned = False
    for row in rows:
        if row['gameID'] == game_id:
            if row['Return Date'] == '--':
                already_returned = False
            else:
                already_returned = True

    return already_returned

def return_game2(game_id, return_date):
    """
    Returns the game by updating the return date in the rental history.

    Parameters:
    - game_id (str): The ID of the game to return.
    - return_date (str): The return date to set for the game.

    Returns:
    - bool: True if the game is successfully returned, False otherwise.
    """
    success = False
    with open('rental.txt', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        header = reader.fieldnames

    for row in rows:
        if row['gameID'] == game_id:
            if row['Return Date'] == '--':
                row['Return Date'] = return_date
                success = True

    # Write the updated data back to the file
    with open('rental.txt', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    return success

# Function to prompt the user to give feedback on a game
def give_feedback(game_id, rating, comment):
    """
    Prompts the user to give feedback on a game, including a rating and comment.

    Parameters:
    - game_ID (str): The ID of the game to give feedback on.
    - rating (str): The rating given by the user.
    - comment (str): The comment provided by the user.

    Returns:
    - bool: True if the feedback is successfully recorded, False otherwise.
    """
    success = False
    feedbackManager.add_feedback(game_id, rating, comment, 'Game_Feedback.txt')
    print("Thank you")
    success = True

    return success

# Main function to execute the game return process
def main():
    """
    The main function that orchestrates the game return process.
    Gets user input, checks if the game has already been returned, returns the game, and asks for feedback.
    """
    # Get game ID and return date from the user
    game_ID = gameID_to_return_prompt()
    return_date = input("Please enter return date")

    # Check if the game has already been returned
    if not already_returned(game_ID):
        return_game2(game_ID, return_date)

    # Ask the user if they want to give feedback
    answer = input("Would you like to give the game feedback? If yes, enter 'yes'")
    if answer.strip().lower() == 'yes':
        rating = input("Enter rating from 1 to 5")
        if 0 <= int(rating) <= 5:
            comment = input("Enter comment")
            give_feedback(game_ID, rating, comment)
        else:
            print("Invalid rating entered")

if __name__ == "__main__":
    main()