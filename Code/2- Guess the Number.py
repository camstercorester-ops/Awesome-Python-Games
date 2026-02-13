# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import math
import simplegui


#------------------------------------------
# declaring global variables
secret_number = 0
upper_bound = 100
remaining_attempts = 0
#------------------------------------------
# helper function to start and restart the game

def start_new_game() -> None:
    """
    Start a new game: pick a secret number in [0, upper_bound) and
    set remaining_attempts to the optimal number of attempts
    (ceiling of log2(upper_bound)).
    """
    global secret_number, remaining_attempts
    
    secret_number = random.randrange(upper_bound)
    # ceil(log2(upper_bound)) via bit_length is already optimal
    remaining_attempts = (upper_bound - 1).bit_length()
    
    # Use a single print call with a pre-formed string for speed
    print("-" * 40 + "\n" + "-" * 40 +
          f"\nNew game. Range is from 0 to {upper_bound}"
          f"\nTotal Guesses: {remaining_attempts}")
#------------------------------------------
# define event handlers for control panel

# Pre-compute ranges for speed
_RANGES = {100, 1000}

def set_game_range(new_upper_bound: int) -> None:
    """Set the number range and start a new game."""
    global upper_bound
    if new_upper_bound not in _RANGES:   # fast membership check
        return
    upper_bound = new_upper_bound
    start_new_game()

# Use lambdas to avoid extra function calls
set_range_to_100  = lambda: set_game_range(100)
set_range_to_1000 = lambda: set_game_range(1000)
reset_game        = start_new_game

def process_player_guess(player_guess: str) -> None:
    """Handle user input: compare guess to secret_number and give feedback."""
    global remaining_attempts

    # Fast-path integer parsing
    if not player_guess.isdigit():
        print("Invalid input! Please enter an integer.")
        return
    guessed_number = int(player_guess)

    print(f"Guess was {guessed_number}")

    # Single comparison chain
    if guessed_number == secret_number:
        print("Correct! You win!")
        start_new_game()
        return

    print("Higher!" if guessed_number < secret_number else "Lower!")
    remaining_attempts -= 1
    print(f"Remaining guesses: {remaining_attempts}")

    if remaining_attempts <= 0:
        print(f"You ran out of guesses. The secret number was {secret_number}.")
        start_new_game()
#------------------------------------------
# Create frame with a descriptive title and optimal size for UX
game_frame = simplegui.create_frame("Guess the Number", 300, 200)

# Add control buttons with consistent width
BUTTON_WIDTH = 150
game_frame.add_button("Range: 0-99", set_range_to_100, BUTTON_WIDTH)
game_frame.add_button("Range: 0-999", set_range_to_1000, BUTTON_WIDTH)
game_frame.add_button("New Game", reset_game, BUTTON_WIDTH)

# Add input field for guesses
game_frame.add_input("Your guess:", process_player_guess, BUTTON_WIDTH)

# Start the first game
start_new_game()

# Start the GUI event loop
game_frame.start()
