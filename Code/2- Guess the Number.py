# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import math
import simplegui


#------------------------------------------
# declaring global variables
secret_number = 0
num_range = 100
remaining_guesses = 0

#------------------------------------------
# helper function to start and restart the game

def new_game():
    """
    Start a new game: pick a secret number in [0, num_range) and
    set remaining_guesses to the optimal number of attempts
    (ceiling of log2(num_range)).
    """
    global secret_number, remaining_guesses
    
    secret_number = random.randrange(num_range)
    remaining_guesses = (num_range - 1).bit_length()
    
    print("\n".join([
        "-" * 40,
        "-" * 40,
        f"New game. Range is from 0 to {num_range}",
        f"Total Guesses: {remaining_guesses}"
    ]))
    
#------------------------------------------
# define event handlers for control panel

def set_range(new_range):
    """Set the number range and start a new game."""
    global num_range
    num_range = new_range
    new_game()

def range100():
    """Button that changes the range to [0,100) and starts a new game."""
    set_range(100)

def range1000():
    """Button that changes the range to [0,1000) and starts a new game."""
    set_range(1000)

def reset():
    """Reset the current game."""
    new_game()

def input_guess(guess: str) -> None:
    """Handle user input: compare guess to secret_number and give feedback."""
    global remaining_guesses

    try:
        guess_int = int(guess)
    except ValueError:
        print("Invalid input! Please enter an integer.")
        return

    print(f"Guess was {guess_int}")

    if guess_int < secret_number:
        print("Higher!")
    elif guess_int > secret_number:
        print("Lower!")
    else:
        print("Correct! You win!")
        new_game()
        return

    remaining_guesses -= 1
    print(f"Remaining guesses: {remaining_guesses}")

    if remaining_guesses <= 0:
        print(f"You ran out of guesses. The secret number was {secret_number}.")
        new_game()

#------------------------------------------
# Create frame with a descriptive title and optimal size for UX
frame = simplegui.create_frame("Guess the Number", 300, 200)

# Add control buttons with consistent width
BTN_WIDTH = 150
frame.add_button("Range: 0-99", range100, BTN_WIDTH)
frame.add_button("Range: 0-999", range1000, BTN_WIDTH)
frame.add_button("New Game", reset, BTN_WIDTH)

# Add input field for guesses
frame.add_input("Your guess:", input_guess, BTN_WIDTH)

# Start the first game
new_game()

# Start the GUI event loop
frame.start()