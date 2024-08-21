"""
F311024 December 2023
This program performs inventory pruning on game data, including analyzing rental history and feedback to identify unpopular games.
It calculates rental frequency, average rental duration, and average rating for each game, applies specified thresholds, and displays a list of unpopular games.
Additionally, it generates and plots three graphs showing average rental duration, rental frequency, and average rating for each game.

Functions:
1. `inventory_pruning()`: Loads rental history and ratings, calculates rental frequency, average rental duration, and average rating for each game.
   Identifies unpopular games based on specified thresholds and displays the list. Plots three graphs showing average rental duration, rental frequency, and average rating.
   Returns:
      - rental_frequency (dict): Dictionary with game ID as keys and rental frequency as values.
      - average_rental_duration (dict): Dictionary with game ID as keys and average rental duration as values.
      - average_rating (dict): Dictionary with game ID as keys and average rating as values.

2. `main()`: The main function that executes inventory pruning.
"""

import matplotlib.pyplot as plt
from datetime import datetime
import csv
import matplotlib

def inventory_pruning():
    #function for inventory pruning

    # Load rental history from a text file using the csv module
    with open('rental.txt', 'r') as file:
        rental_history_reader = csv.reader(file)
        header = next(rental_history_reader) # Skip the header row if it exists

        rental_history = [
            {
                "gameID": row[0],
                "Rental Date": row[1],
                "Return Date": row[2],
                "Customer": row[3]
            }
            for row in rental_history_reader
        ]

    # Load ratings from a text file using the csv module
    with open('Game_Feedback.txt', 'r') as file:
        ratings_reader = csv.reader(file)
        header = next(ratings_reader) # Skip the header row if it exists

        ratings = [
            {
                "GameID": row[0],
                "Rating": int(row[1]),
                "Comments": row[2]
            }
            for row in ratings_reader
        ]

    # Calculate rental frequency
    rental_frequency = {}
    for rental in rental_history:
        game_id = rental["gameID"]
        rental_frequency[game_id] = rental_frequency.get(game_id, 0) + 1

    # Calculate average rental duration
    average_rental_duration = {}
    for rental in rental_history:
        game_id = rental["gameID"]
        rental_date = datetime.strptime(rental['Rental Date'], '%d/%m/%Y')
        return_date_str = rental['Return Date']
        if return_date_str != "--":
            return_date = datetime.strptime(return_date_str, '%d/%m/%Y')
            rental_duration = (return_date - rental_date).days
            average_rental_duration[game_id] = (
                average_rental_duration.get(game_id, 0) + rental_duration
            )

    for game_id, total_duration in average_rental_duration.items():
        rental_frequency_game = rental_frequency.get(game_id, 1) # Avoid division by zero
        average_rental_duration[game_id] = total_duration / rental_frequency_game

    # Calculate average rating
    average_rating = {}
    for rating in ratings:
        game_id = rating["GameID"]
        average_rating[game_id] = average_rating.get(game_id, 0) + rating["Rating"]

    # Calculate the average rating for each game
    for game_id, total_rating in average_rating.items():
        rental_frequency_game = rental_frequency.get(game_id, 1) # Avoid division by zero
        average_rating[game_id] = total_rating / rental_frequency_game

    # Identify unpopular games based on your criteria
    threshold1 = 3
    threshold2 = 8
    threshold3 = 2

    unpopular_games = [
        game_id for game_id in rental_frequency
        if (rental_frequency.get(game_id, 0) < threshold1) and
           (average_rental_duration.get(game_id, 0) < threshold2) and
           (average_rating.get(game_id, 0) < threshold3)
    ]

    # Display the list of unpopular games
    print("these are games you can consider for removal:")
    print(unpopular_games)

    # Plotting Graphs
    
    # Plotting Average Rental Duration
    plt.figure(figsize=(10, 5))
    plt.bar(average_rental_duration.keys(), average_rental_duration.values())
    plt.xlabel('Game ID')
    plt.ylabel('Average Rental Duration')
    plt.title('Average Rental Duration of Each Game')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability


    # Plotting Rental Frequency
    plt.figure(figsize=(10, 5))
    plt.bar(rental_frequency.keys(), rental_frequency.values())
    plt.xlabel('Game ID')
    plt.ylabel('Rental Frequency')
    plt.title('Rental Frequency of Each Game')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability


    # Plotting Average Rating
    plt.figure(figsize=(10, 5))
    plt.bar(average_rating.keys(), average_rating.values())
    plt.xlabel('Game ID')
    plt.ylabel('Average Rating')
    plt.title('Average Rating of Each Game')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

    #formatting so more neat
    plt.tight_layout()

    #showing graphs
    plt.show()
    return rental_frequency, average_rental_duration, average_rating

def main():
    inventory_pruning()

if __name__ == "__main__":
    main()