# Rock-paper-scissors-lizard-Spock template
# A Python implementation of the classic Rock-Paper-Scissors-Lizard-Spock game
# This variant was popularized by The Big Bang Theory and adds two extra moves
# to the traditional Rock-Paper-Scissors game for more complex gameplay.

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
#
# This numerical representation allows for mathematical determination
# of the winner using modular arithmetic.

#----------------------------------------------------------
# Helper functions section
#----------------------------------------------------------
#----------------------------------------------------------

import random
import tkinter as tk
from typing import Dict, Optional, Tuple

# Module-level constant for conversion
# Maps string move names to their corresponding numerical values
MOVE_TO_NUMBER: Dict[str, int] = {
    "rock": 0,
    "spock": 1,
    "paper": 2,
    "lizard": 3,
    "scissors": 4
}

# Add reverse mapping constant
# Maps numerical values back to their string move names for display purposes
NUMBER_TO_MOVE: Dict[int, str] = {v: k for k, v in MOVE_TO_NUMBER.items()}

# Game constants
# Frozen set of all valid move names for efficient membership testing
VALID_MOVES = frozenset(['rock', 'paper', 'scissors', 'lizard', 'spock'])
# Set of differences that result in computer winning (see rpsls function for details)
WINNING_DIFFS = {1, 2}
# Difference value that indicates a tie game
TIE_DIFF = 0

# helper functions


def _validate_choice(choice: str) -> None:
    """
    Validate that the player's choice is a valid move.
    
    Args:
        choice (str): The player's move selection to validate
        
    Raises:
        ValueError: If choice is not a string or not a valid move name
    """
    if not isinstance(choice, str):
        raise ValueError("Choice must be a string")
    if choice.lower() not in MOVE_TO_NUMBER:
        raise ValueError(f"Invalid choice. Valid moves are: {', '.join(MOVE_TO_NUMBER)}")


def _determine_winner(diff: int) -> str:
    """
    Determine the game outcome based on the modular difference.

    Args:
        diff (int): The modular difference (comp_number - player_number) % 5

    Returns:
        str: "Computer Wins", "Player Wins", or "Player and computer tie!"
    """
    return (
        "Computer Wins" if diff in WINNING_DIFFS else
        "Player and computer tie!" if diff == TIE_DIFF else
        "Player Wins"
    )


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
    try:
        return MOVE_TO_NUMBER[name.lower()]
    except (AttributeError, KeyError):
        raise ValueError(
            f"'{name}' is not a valid move. "
            f"Valid moves are: {', '.join(MOVE_TO_NUMBER)}"
        ) from None

#----------------------------------------------------------
# Number to name conversion function
#----------------------------------------------------------

        
def number_to_name(number: int) -> str:
    """
    Convert a numeric input to its corresponding name in the Rock-Paper-Scissors-Lizard-Spock game.

    This is the inverse operation of name_to_number(), allowing conversion
    from the internal numerical representation back to human-readable move names.

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
    if not 0 <= number <= 4:
        raise ValueError(f"Invalid number {number!r}. Must be an integer between 0 and 4")
    return NUMBER_TO_MOVE[number]
    
#----------------------------------------------------------    
# Main game function
#----------------------------------------------------------    

def rpsls(player_choice: str) -> Optional[Tuple[str, str, str]]:
    """
    Play a game of Rock-Paper-Scissors-Lizard-Spock against the computer.
    
    Implements the complete game logic including:
    - Input validation
    - Random computer move generation
    - Winner determination using modular arithmetic
    - Console output of game results
    
    Game Rules (using modular arithmetic):
    The winner is determined by (computer_number - player_number) % 5:
    - If result is 1 or 2: Computer wins
    - If result is 3 or 4: Player wins
    - If result is 0: Tie game
    
    This mathematical approach encodes all the complex winning relationships
    between the five different moves.
    
    Args:
        player_choice (str): The player's choice from VALID_MOVES
        
    Returns:
        Optional[Tuple[str, str, str]]: (player_choice, computer_choice, result)
                                       None if input is invalid
        
    Raises:
        ValueError: If player_choice is not one of the valid options
        
    Console Output:
        Prints a formatted game summary including both choices and the result
    """
    try:
        _validate_choice(player_choice)
        player_number = name_to_number(player_choice)
        comp_number = random.randrange(5)
        comp_choice = number_to_name(comp_number)
        result = _determine_winner((comp_number - player_number) % 5)

        # UI output
        print("------------")
        print("Player chooses", player_choice)
        print("Computer chooses", comp_choice)
        print(result)

        return player_choice, comp_choice, result

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

    Acts as a bridge between the GUI input field and the core game logic.
    Handles any validation errors that may occur during game processing.
    
    Args:
        inp (str): The user's input string representing their choice.
        
    Returns:
        Optional[bool]: True if input was valid and processed successfully,
                       False if input validation failed,
                       None if an unexpected error occurred
    """
    try:
        rpsls(inp)
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False


def create_gui() -> tk.Tk:
    """
    Create and configure the graphical user interface for the game.
    
    Builds a simple tkinter window with:
    - Input field for entering move choices
    - Submit button to process the input
    - Basic window styling and layout
    
    Returns:
        tk.Tk: The configured tkinter window object ready for mainloop()
        
    Note:
        The GUI provides a user-friendly alternative to command-line input
    """
    window = tk.Tk()
    window.title("Rock-paper-scissors-lizard-Spock")
    window.geometry("200x200")
    
    input_field = tk.Entry(window)
    input_field.pack(pady=10)
    
    def on_submit():
        """Handle submit button click by processing input and clearing field."""
        get_input(input_field.get())
        input_field.delete(0, tk.END)
    
    submit_button = tk.Button(window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)
    
    return window


# Create and start the GUI
# This conditional ensures the GUI only launches when the script is run directly,
# not when imported as a module in other Python code
if __name__ == "__main__":
    window = create_gui()
    window.mainloop()
