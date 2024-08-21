
"""
F311024 December 2023
This program provides functions for checking the existence of games and customers, managing game rentals, and executing the game renting process.

Functions:
1. `game_exists(gameID)`: Checks if a game with the given ID exists in the "game_info.txt" file.


2. `customer_exists(customer_id)`: Checks if a customer with the given ID exists in the "Subscription_Info.txt" file.
   

3. `customer_ID_prompt()`: Gets customer ID from user input.
   

4. `get_sub_type(customerID)`: Gets the subscription type for a given customer ID from "Subscription_Info.txt".
   

5. `check_number_rented(customerID)`: Checks the number of games rented by a customer based on their ID.
   

6. `rentgame2(gameID, customerID, date)`: Rents a game for a customer and updates "rental.txt".
 

7. `ask_for_date()`: Gets the current date from user input.
   

8. `main()`: Main function to execute the game renting process.
   Gets user input, checks if the customer and game exist, rents the game, and provides appropriate feedback.
"""

import database
import csv
import subscriptionManager
import gamesearch

# Function to check if a game with the given ID exists in the game_info.txt file
def game_exists(gameID):
    """
    Checks if a game with the given ID exists in the game_info.txt file.

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

# Function to check if a customer with the given ID exists in the Subscription_Info.txt file
def customer_exists(customer_id):
    """
    Checks if a customer with the given ID exists in the Subscription_Info.txt file.

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

# Function to prompt the user for a customer ID
def customer_ID_prompt():
    """
    Gets customer ID from user input.

    Returns:
    - str: The entered customer ID.
    """
    return input("Please enter your customer ID: ")

# Function to get the subscription type for a given customer ID from Subscription_Info.txt
def get_sub_type(customerID):
    """
    Gets the subscription type for a given customer ID from Subscription_Info.txt.

    Parameters:
    - customerID (str): The ID of the customer.

    Returns:
    - str: The subscription type of the customer.
    """
    sub_info = ''
    with open("Subscription_Info.txt", 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            if row['CustomerID'].lower() == customerID.lower():
                print(row)
                sub_info = row['SubscriptionType']
                break
    return sub_info

# Function to check the number of games rented by a customer based on their ID
def check_number_rented(customerID):
    """
    Checks the number of games rented by a customer based on their ID.

    Parameters:
    - customerID (str): The ID of the customer.

    Returns:
    - int: The number of games rented by the customer.
    """
    number = 0
    with open("rental.txt", 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            if row['Customer'].lower() == customerID.lower():
                if row['Return Date'] == '--':
                    number += 1
    return number

# Function to rent a game for a customer and update rental.txt
def rentgame2(gameID, customerID, date):
    """
    Rents a game for a customer and updates rental.txt.

    Parameters:
    - gameID (str): The ID of the game to be rented.
    - customerID (str): The ID of the customer renting the game.
    - date (str): The current date of the rental.

    Returns:
    - bool: True if the game is successfully rented, False otherwise.
    """
    success = False
    subscriptions = subscriptionManager.load_subscriptions("Subscription_Info.txt")
    if subscriptionManager.check_subscription(customerID, subscriptions):
        info = get_sub_type(customerID)
        limit = subscriptionManager.get_rental_limit(info)
        number = check_number_rented(customerID)
        if number >= limit:
            print("Cannot rent any more games. Rental limit reached.")
        else:
            available = gamesearch.check_availability(gameID)
            if available:
                fieldnames = ['gameID', 'Rental Date', 'Return Date', 'Customer']
                with open("rental.txt", 'a', newline='') as file:
                    writer = csv.writer(file)

                    # Write the new row to the file
                    writer.writerow([gameID, date, '--', customerID])
                    return True  # Successfully rented the game
            else:
                print("Game is not available for rent.")
    else:
        print("Subscription is no longer active.")
    return False  # Game rental failed

# Function to get the current date from user input
def ask_for_date():
    """
    Gets the current date from user input.

    Returns:
    - str: The entered current date.
    """
    return input("What is the current date?: ")

# Main function to execute the game renting process
def main():
    """
    Main function to execute the game renting process.
    Gets user input, checks if the customer and game exist, rents the game, and provides appropriate feedback.
    """
    customerID = customer_ID_prompt()
    if database.customer_exists(customerID):
        date = ask_for_date()
        gameID = gamesearch.enter_game_ID()
        if database.game_exists(gameID):
            if rentgame2(gameID, customerID, date):
                print("Game rented successfully.")
        else:
            print("Game does not exist.")
    else:
        print("Customer does not exist.")

# Execute the main function if the script is run
if __name__ == "__main__":
    main()