"""
F311024 December 2023
This program provides functions for managing game data, checking game availability, and verifying customer and game existence.

Functions:
1. `read_game_data()
2. `check_availability_print(game_ID)
3. `customer_exists(customer_id)
4. `game_exists(gameID)`
"""

import csv
import datetime

def read_game_data():
    """
    Reads game data from the "game_info.txt" file into a list of dictionaries.

    Returns:
    - list: A list of dictionaries, each representing a game with attributes like ID, Platform, Genre, Title, Publisher, and Purchase Date.
    """
    games = []

    with open("game_info.txt", 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            games.append({
                'ID': row['ID'],
                'Platform': row['Platform'],
                'Genre': row['Genre'],
                'Title': row['Title'],
                'Publisher': row['Publisher'],
                'Purchase Date': row['Purchase Date']
            }) 
    return games 

def check_availability_print(game_ID):
    """
    Checks and prints the availability of a game with the specified ID in the "rental.txt" file.

    Parameters:
    - game_ID (str): The ID of the game to check for availability.
    """
    with open("rental.txt", 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            if row['gameID'].lower() == game_ID.lower():
                return_date = row['Return Date']
                if return_date.strip() == '--':
                    print("Game is not available")
                else:
                    print("Game is available")
                break

def customer_exists(customer_id):
    """
    Checks if a customer with the given ID exists in the "Subscription_Info.txt" file.

    Parameters:
    - customer_id (str): The ID of the customer to check for existence.

    Returns:
    - bool: True if the customer exists, False otherwise.
    """
    with open("Subscription_Info.txt", 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if row and row[0] == customer_id:
                return True
    return False

def game_exists(gameID):
    """
    Checks if a game with the given ID exists in the "game_info.txt" file.

    Parameters:
    - gameID (str): The ID of the game to check for existence.

    Returns:
    - bool: True if the game exists, False otherwise.
    """
    with open("game_info.txt", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'ID' in row and row['ID'] == gameID:
                return True
    return False