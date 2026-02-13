# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

#----------------------------------------------------------
# Helper functions section
#----------------------------------------------------------
#----------------------------------------------------------

import random
import tkinter as tk

# helper functions

def name_to_number(name):
    """
    Convert a rock-paper-scissors-lizard-Spock name to its corresponding number.
    
    The conversion follows the standard mapping:
    - rock -> 0
    - Spock -> 1
    - paper -> 2
    - lizard -> 3
    - scissors -> 4
    
    Args:
        name (str): The name of the move to convert (case-sensitive).
        
    Returns:
        int: The number corresponding to the input name (0-4).
        
    Side Effects:
        Prints an error message if the input name is not valid.
        
    Examples:
        >>> name_to_number("rock")
        0
        >>> name_to_number("Spock")
        1
    """
    
    if not isinstance(name, str):
        raise ValueError("Input must be a string")
        
    conversion = {
        "rock": 0,
        "Spock": 1,
        "paper": 2,
        "lizard": 3,
        "scissors": 4
    }
    
    if name not in conversion:
        raise ValueError(f"'{name}' is not a valid move. Valid moves are: {', '.join(conversion.keys())}")
    
    return conversion[name]

#----------------------------------------------------------
# Number to name conversion function
#----------------------------------------------------------
        
def number_to_name(number):
    """
    Convert a numeric input to its corresponding name in the Rock-Paper-Scissors-Lizard-Spock game.
    
    Parameters:
        number (int): A numeric value between 0 and 4 representing:
                    0 - rock
                    1 - Spock 
                    2 - paper
                    3 - lizard
                    4 - scissors
    
    Returns:
        str: The name corresponding to the input number if valid
            None (implicitly) if the number is invalid (prints error message)
    
    Prints:
        Error message if the input number is not between 0 and 4
    
    Examples:
        >>> number_to_name(0)
        'rock'
        >>> number_to_name(3)
        'lizard'
    """
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock" 
    elif number == 2:
        return "paper" 
    elif number == 3:
        return "lizard" 
    elif number == 4:
        return "scissors" 
    else:
        print("Error: Not a valid number")

    
#----------------------------------------------------------    
# Main game function
#----------------------------------------------------------    

def rpsls(player_choice):
    """
    Play a game of Rock-Paper-Scissors-Lizard-Spock against the computer.
    
    This function implements the Rock-Paper-Scissors-Lizard-Spock game where
    the player chooses one of five options and competes against a randomly
    selected computer choice. The game follows these rules:
    - Scissors cuts Paper
    - Paper covers Rock
    - Rock crushes Lizard
    - Lizard poisons Spock
    - Spock smashes Scissors
    - Scissors decapitates Lizard
    - Lizard eats Paper
    - Paper disproves Spock
    - Spock vaporizes Rock
    - Rock crushes Scissors
    
    Parameters:
    player_choice (str): The player's choice. Must be one of:
                        'rock', 'paper', 'scissors', 'lizard', or 'spock'
                        
    Returns:
    None: The function prints the game results but doesn't return anything.
    
    Side Effects:
    - Prints game headers
    - Prints player and computer choices
    - Prints game result (winner or tie)
    
    Raises:
    ValueError: If player_choice is not one of the valid options
    """
    
    print("------------")
    print("------------")    
    
    print("Player chooses " + player_choice)
    
    try:
        player_number = name_to_number(player_choice)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    comp_number = random.randrange(0,5)
    
    comp_choice = number_to_name(comp_number)
    
    print("Computer chooses ", comp_choice)
    
    diff = (comp_number - player_number) % 5

    if diff == 1 or diff == 2:
        print("Computer Wins")
    
    elif diff == 3 or diff == 4:
        print("Player Wins")
    
    else:
        print("Player and computer tie!")
 
#----------------------------------------------------------
# GUI setup section
#----------------------------------------------------------
#----------------------------------------------------------    
#----------------------------------------------------------    
    
# Event Handlers

def get_input(inp):
    """
    Process the user input for the Rock-Paper-Scissors-Lizard-Spock game.

    This function validates the input string against the valid options 
    (rock, paper, lizard, Spock, scissors) and either calls the game function 
    with valid input or prints an error message for invalid input.

    Args:
        inp (str): The user's input string representing their choice.

    Returns:
        None: The function either calls rpsls() or prints an error message.
    
    Side Effects:
        - Calls rpsls() function if input is valid
        - Prints error message if input is invalid
    """
    
    if (inp == "rock" or inp == "paper" or inp == "lizard" or inp == "Spock" or inp == "scissors"):
        rpsls(inp)
    else:
        print("Error: Invalid Input")

# Creating a Window
window = tk.Tk()
window.title("Rock-paper-scissors-lizard-Spock")
window.geometry("200x200")

# Creating an input field and button
input_field = tk.Entry(window)
input_field.pack()

def on_submit():
    get_input(input_field.get())
    input_field.delete(0, tk.END)

submit_button = tk.Button(window, text="Submit", command=on_submit)
submit_button.pack()

# Starting the Window
window.mainloop()
    
"""	
# Test cases section
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
"""