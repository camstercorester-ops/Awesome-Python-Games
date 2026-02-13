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
from typing import Dict, Optional, Tuple

# Module-level constant for conversion
MOVE_TO_NUMBER: Dict[str, int] = {
    "rock": 0,
    "spock": 1,
    "paper": 2,
    "lizard": 3,
    "scissors": 4
}

# Add reverse mapping constant
NUMBER_TO_MOVE: Dict[int, str] = {v: k for k, v in MOVE_TO_NUMBER.items()}

# Game constants
VALID_MOVES = frozenset(['rock', 'paper', 'scissors', 'lizard', 'spock'])
WINNING_DIFFS = {1, 2}
TIE_DIFF = 0

# helper functions

def _validate_choice(choice: str) -> None:
    """Validate player's choice."""
    if not isinstance(choice, str):
        raise ValueError("Choice must be a string")
    if choice.lower() not in VALID_MOVES:
        raise ValueError(f"Invalid choice. Valid moves are: {', '.join(VALID_MOVES)}")

def _determine_winner(diff: int) -> str:
    """Determine the winner based on the difference."""
    if diff in WINNING_DIFFS:
        return "Computer Wins"
    if diff == TIE_DIFF:
        return "Player and computer tie!"
    return "Player Wins"

def name_to_number(name: str) -> int:
    """
    Convert a rock-paper-scissors-lizard-Spock name to its corresponding number.
    
    The conversion follows the standard mapping:
    - rock -> 0
    - Spock -> 1
    - paper -> 2
    - lizard -> 3
    - scissors -> 4
    
    Args:
        name (str): The name of the move to convert (case-insensitive).
        
    Returns:
        int: The number corresponding to the input name (0-4).
        
    Raises:
        ValueError: If input is not a string or not a valid move name.
        
    Examples:
        >>> name_to_number("rock")
        0
        >>> name_to_number("Spock")
        1
    """
    if not isinstance(name, str):
        raise ValueError("Input must be a string")
    
    # Convert to lowercase for case-insensitive comparison
    name_lower = name.lower()
    
    # Use dictionary.get() with default None for invalid moves
    result = MOVE_TO_NUMBER.get(name_lower)
    
    if result is None:
        raise ValueError(
            f"'{name}' is not a valid move. "
            f"Valid moves are: {', '.join(MOVE_TO_NUMBER.keys())}"
        )
    
    return result

#----------------------------------------------------------
# Number to name conversion function
#----------------------------------------------------------
        
def number_to_name(number: int) -> str:
    """
    Convert a numeric input to its corresponding name in the Rock-Paper-Scissors-Lizard-Spock game.
    
    Args:
        number (int): A numeric value between 0 and 4 representing:
                     0 - rock
                     1 - spock
                     2 - paper
                     3 - lizard
                     4 - scissors
    
    Returns:
        str: The name corresponding to the input number.
    
    Raises:
        ValueError: If the input number is not between 0 and 4.
    
    Examples:
        >>> number_to_name(0)
        'rock'
        >>> number_to_name(3)
        'lizard'
    """
    if not isinstance(number, int):
        raise ValueError("Input must be an integer")
        
    try:
        return NUMBER_TO_MOVE[number]
    except KeyError:
        raise ValueError(f"Invalid number {number}. Must be between 0 and 4")

    
#----------------------------------------------------------    
# Main game function
#----------------------------------------------------------    

def rpsls(player_choice: str) -> Optional[Tuple[str, str, str]]:
    """
    Play a game of Rock-Paper-Scissors-Lizard-Spock against the computer.
    
    Args:
        player_choice (str): The player's choice from VALID_MOVES
        
    Returns:
        Optional[Tuple[str, str, str]]: (player_choice, computer_choice, result)
                                       None if input is invalid
        
    Raises:
        ValueError: If player_choice is not one of the valid options
    """
    try:
        _validate_choice(player_choice)
        player_number = name_to_number(player_choice)
        comp_number = random.randrange(5)
        comp_choice = number_to_name(comp_number)
        diff = (comp_number - player_number) % 5
        result = _determine_winner(diff)
        
        # UI output
        print("------------")
        print("Player chooses", player_choice)
        print("Computer chooses", comp_choice)
        print(result)
        
        return (player_choice, comp_choice, result)
        
    except ValueError as e:
        print(f"Error: {e}")
        return None
 
#----------------------------------------------------------
# GUI setup section
#----------------------------------------------------------
#----------------------------------------------------------    
#----------------------------------------------------------    
    
# Event Handlers

def get_input(inp: str) -> Optional[bool]:
    """
    Process the user input for the Rock-Paper-Scissors-Lizard-Spock game.

    Args:
        inp (str): The user's input string representing their choice.
        
    Returns:
        Optional[bool]: True if input was valid and processed, False otherwise.
    """
    try:
        rpsls(inp)
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False

def create_gui() -> tk.Tk:
    """Create and configure the game GUI."""
    window = tk.Tk()
    window.title("Rock-paper-scissors-lizard-Spock")
    window.geometry("200x200")
    
    input_field = tk.Entry(window)
    input_field.pack(pady=10)
    
    def on_submit():
        get_input(input_field.get())
        input_field.delete(0, tk.END)
    
    submit_button = tk.Button(window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)
    
    return window

# Create and start the GUI
if __name__ == "__main__":
    window = create_gui()
    window.mainloop()