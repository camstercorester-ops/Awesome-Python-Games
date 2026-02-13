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

def input_guess(guess):
    """Handle user input: compare guess to secret_number and give feedback."""
    global remaining_guesses

    try:
        guess = int(guess)
    except ValueError:
        print("Invalid input! Please enter an integer.")
        return

    print(f"Guess was {guess}")

    if guess < secret_number:
        print("Higher!")
    elif guess > secret_number:
        print("Lower!")
    else:
        print("Correct!")
        new_game()
        return

    remaining_guesses -= 1
    print(f"\nNumber of remaining guesses is: {remaining_guesses}")

    if remaining_guesses == 0:
        print(f"You ran out of guesses :(  The secret number was {secret_number}")
        new_game()

#------------------------------------------
        
# create frame

frame = simplegui.create_frame("Guess the Number", 200, 200)

#------------------------------------------

# register event handlers for control elements and start frame

frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

frame.add_button("New Game", reset, 200)

#------------------------------------------
# call new_game 
new_game()

#------------------------------------------
# starting the frame
frame.start()
#------------------------------------------




# always remember to check your completed program against the grading rubric
