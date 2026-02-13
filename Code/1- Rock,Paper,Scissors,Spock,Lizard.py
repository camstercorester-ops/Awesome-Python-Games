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
#----------------------------------------------------------
#----------------------------------------------------------

import random
import simplegui

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

    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "Error: Not a valid name" 

#----------------------------------------------------------
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
        print "Error: Not a valid number" 
    
#----------------------------------------------------------    
#----------------------------------------------------------    


def rpsls(player_choice): 
    
    print "------------"
    print "------------"    
    
    print "Player chooses " + player_choice 
    
    player_number = name_to_number(player_choice)
    
	comp_number = random.randrange(0,5)
    
    comp_choice = number_to_name(comp_number)
    
    print "Computer chooses " + comp_choice 
    
    diff = (comp_number - player_number) % 5

    if diff == 1 or diff == 2:
        print "Computer Wins"
    elif diff == 3 or diff == 4:
        print "Player Wins"
    else:
        print "Player and computer tie!"
 

#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------    
#----------------------------------------------------------    
    
	
# Event Handlers

def get_input(inp):
	
	if (inp == "rock" or inp == "paper" or inp == "lizard" or 
			inp == "Spock" or inp == "scissors"):		
		rpsls(inp)
	else:
		print "Error: Invalid Input"
	
	


# Creating a Frame

frame = simplegui.create_frame("Rock-paper-scissors-lizard-Spock",200,200)

# Registering Handlers

frame.add_input("Enter your choice: ", get_input,200)	
	
	
# Starting the Frame

frame.start()	
    

	
"""	
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
"""

# always remember to check your completed program against the grading rubric


