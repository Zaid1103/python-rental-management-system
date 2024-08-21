
"""
F311024 December 2023
This program facilitates game searches, checks the availability of specific games, and prints details based on user input.
It interacts with a database of game information, allowing users to search by title, genre, or platform.
The program also checks the availability of a specific game based on its ID and provides relevant information.

Functions:
1. `search_prompt()`: Prompts the user for search criteria and returns a tuple containing the search term and option chosen by the user.
   

2. `search_game_by_title(games, search)`: Searches for games by title in the provided list of game data dictionaries.
   

3. `search_game_by_genre(games, search)`: Searches for games by genre in the provided list of game data dictionaries.
   

4. `search_game_by_platform(games, search)`: Searches for games by platform in the provided list of game data dictionaries.
  

5. `enter_game_ID()`: Prompts the user for a game ID and returns the entered game ID.
   

6. `check_availability(game_ID)`: Checks the availability of a specific game based on its ID by reading the rental history from a file.
   

7. `print_results(game)`: Prints the details of a game, such as ID, platform, genre, title, publisher, and purchase date.
   

8. `main()`: The main function that orchestrates the entire script.
   Reads game data, performs searches, checks availability, and prints results based on user input.
"""


import csv
from database import read_game_data

# Function to prompt the user for search criteria
def search_prompt():
    """
    Prompts the user for search criteria and returns a tuple containing the search term and option chosen by the user.

    Returns:
    - tuple: A tuple containing the search term and the option chosen by the user.
    """
    user_input = int(input("\nSearch by title: 1, Search by Genre: 2, Search by Platform: 3"))

    if user_input == 1:
        option = 1
        title = input("Enter game title")
        return title, option
    elif user_input == 2:
        option = 2
        genre = input("Enter game genre")
        return genre, option
    elif user_input == 3:
        option = 3
        platform = input("Enter platform")
        return platform, option

# Function to search games by title
def search_game_by_title(games, search):
    """
    Searches for games by title in the provided list of game data dictionaries.

    Parameters:
    - games (list of dictionaries): List of game data dictionaries.
    - search (str): Search term for the game title.

    Returns:
    - list: List of dictionaries representing games that match the search criteria.
    """
    results = []
    for game in games:
        if search.strip().lower() == game['Title'].strip().lower():
            results.append(game)
    return results

# Function to search games by genre
def search_game_by_genre(games, search):
    """
    Searches for games by genre in the provided list of game data dictionaries.

    Parameters:
    - games (list of dictionaries): List of game data dictionaries.
    - search (str): Search term for the game genre.

    Returns:
    - list: List of dictionaries representing games that match the search criteria.
    """
    results = []
    for game in games:
        if search.strip().lower() == game['Genre'].strip().lower():
            results.append(game)
    return results

# Function to search games by platform
def search_game_by_platform(games, search):
    """
    Searches for games by platform in the provided list of game data dictionaries.

    Parameters:
    - games (list of dictionaries): List of game data dictionaries.
    - search (str): Search term for the game platform.

    Returns:
    - list: List of dictionaries representing games that match the search criteria.
    """
    results = []
    for game in games:
        if search.strip().lower() == game['Platform'].strip().lower():
            results.append(game)
    return results

# Function to prompt the user for a game ID
def enter_game_ID():
    """
    Prompts the user for a game ID and returns the entered game ID.

    Returns:
    - str: The entered game ID.
    """
    game_ID = input("Enter game ID to check for availability")
    return game_ID

# Function to check the availability of a game based on its ID
def check_availability(game_ID):
    """
    Checks the availability of a specific game based on its ID by reading the rental history from a file.

    Parameters:
    - game_ID (str): The ID of the game to check for availability.

    Returns:
    - bool: True if the game is available, False otherwise.
    """
    with open("rental.txt", 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            if row['gameID'].lower() == game_ID.lower():
                return_date = row['Return Date']
                if return_date.strip() == '--':
                    availability = False  # Game is not available
                else:
                    availability = True  # Game is available
    return availability

# Function to print the details of a game
def print_results(game):
    """
    Prints the details of a game, such as ID, platform, genre, title, publisher, and purchase date.

    Parameters:
    - game (dictionary): A dictionary containing details of a game.
    """
    print(f"ID: {game['ID']}")
    print(f"Platform: {game['Platform']}")
    print(f"Genre: {game['Genre']}")
    print(f"Title: {game['Title']}")
    print(f"Publisher: {game['Publisher']}")
    print(f"Purchase Date: {game['Purchase Date']}")
    print()

# Main function
def main():
    """
    The main function that orchestrates the entire script.
    Reads game data, performs searches, checks availability, and prints results based on user input.
    """
    games = read_game_data()

    # Get search criteria from the user
    result_tuple = search_prompt()
    term, input_option = result_tuple

    # Perform the search based on user input
    if input_option == 1:
        results = search_game_by_title(games, term)
        for result in results:
            print_results(result)
    elif input_option == 2:
        results = search_game_by_genre(games, term)
        for result in results:
            print_results(result)
    elif input_option == 3:
        results = search_game_by_platform(games, term)
        for result in results:
            print_results(result)

    # Check availability of a specific game based on user input
    game_ID = enter_game_ID()

    if check_availability(game_ID):
        print("Game is available")
    else:
        print("Game is not available")

# Execute the main function if the script is run
if __name__ == "__main__":
    main()