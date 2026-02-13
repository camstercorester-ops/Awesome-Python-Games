# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import math
import tkinter as tk
from tkinter import ttk

#------------------------------------------
# declaring global variables
secret_number = 0
upper_bound = 100
remaining_attempts = 0
best_score = {100: None, 1000: None}  # track best scores per range
total_games = 0
total_wins = 0
history = []  # store last few guesses for hints
#------------------------------------------
# helper function to start and restart the game


def start_new_game() -> None:
    """
    Start a new game: pick a secret number in [0, upper_bound) and
    set remaining_attempts to the optimal number of attempts
    (ceiling of log2(upper_bound)).
    """
    global secret_number, remaining_attempts, history
    secret_number = random.randrange(upper_bound)
    remaining_attempts = (upper_bound - 1).bit_length()
    history = []  # reset guess history
    update_status()


def update_status():
    """Refresh the status label with current game info."""
    status = (f"Range: 0-{upper_bound-1}  |  "
              f"Guesses left: {remaining_attempts}  |  "
              f"Wins: {total_wins}/{total_games}")
    if best_score[upper_bound] is not None:
        status += f"  |  Best: {best_score[upper_bound]}"
    status_var.set(status)

#------------------------------------------
# define event handlers for control panel


_RANGES = {100, 1000}


def set_game_range(new_upper_bound: int) -> None:
    """Set the number range and start a new game."""
    global upper_bound
    if new_upper_bound not in _RANGES:
        return
    upper_bound = new_upper_bound
    start_new_game()


set_range_to_100 = lambda: set_game_range(100)
set_range_to_1000 = lambda: set_game_range(1000)
reset_game = start_new_game


def process_player_guess(player_guess: str) -> None:
    """Handle user input: compare guess to secret_number and give feedback."""
    global remaining_attempts, total_games, total_wins, best_score
    if not player_guess.isdigit():
        print("Invalid input! Please enter an integer.")
        return
    guessed_number = int(player_guess)
    if guessed_number < 0 or guessed_number >= upper_bound:
        print(f"Out of range! Pick between 0 and {upper_bound-1}.")
        return

    history.append(guessed_number)
    print(f"Guess was {guessed_number}")
    remaining_attempts -= 1

    if guessed_number == secret_number:
        total_wins += 1
        used = ((upper_bound - 1).bit_length()) - remaining_attempts
        print(f"Correct! You win in {used} guesses!")
        if best_score[upper_bound] is None or used < best_score[upper_bound]:
            best_score[upper_bound] = used
            print("New best score for this range!")
        start_new_game()
        return

    print("Higher!" if guessed_number < secret_number else "Lower!")
    if history:
        warmer = None
        if len(history) >= 2:
            prev_dist = abs(history[-2] - secret_number)
            curr_dist = abs(history[-1] - secret_number)
            warmer = "Warmer" if curr_dist < prev_dist else "Colder"
        if warmer:
            print(warmer)
    print(f"Remaining guesses: {remaining_attempts}")

    if remaining_attempts <= 0:
        total_games += 1
        print(f"You ran out of guesses. The secret number was {secret_number}.")
        start_new_game()


def get_hint():
    """Reveal one bit of information: parity."""
    if secret_number % 2 == 0:
        print("Hint: The secret number is even.")
    else:
        print("Hint: The secret number is odd.")
    hint_button.config(state="disabled")


#------------------------------------------
# Build UI
root = tk.Tk()
root.title("Guess the Number")
root.geometry("400x420")
root.configure(bg="#f0f0f8")

status_var = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_var, anchor="w")
status_label.pack(fill="x", padx=10, pady=5)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

range_frame = ttk.Frame(root)
range_frame.pack(fill="x", padx=10, pady=5)
ttk.Button(range_frame, text="Range: 0-99", command=set_range_to_100).pack(side="left", padx=5)
ttk.Button(range_frame, text="Range: 0-999", command=set_range_to_1000).pack(side="left", padx=5)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

ttk.Label(root, text="Enter your guess:").pack(anchor="w", padx=10)
guess_entry = ttk.Entry(root)
guess_entry.pack(fill="x", padx=10, pady=5)
guess_entry.bind("<Return>", lambda e: process_player_guess(guess_entry.get()))

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

action_frame = ttk.Frame(root)
action_frame.pack(fill="x", padx=10, pady=5)
hint_button = ttk.Button(action_frame, text="Get a Hint (once/game)", command=get_hint)
hint_button.pack(side="left", padx=5)
ttk.Button(action_frame, text="New Game", command=reset_game).pack(side="left", padx=5)

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

history_var = tk.StringVar(value="Recent guesses: None")
history_label = ttk.Label(root, textvariable=history_var, anchor="w")
history_label.pack(fill="x", padx=10, pady=5)


def update_history():
    if history:
        history_var.set("Recent guesses: " + ", ".join(map(str, history[-5:])))
    else:
        history_var.set("Recent guesses: None")


old_process = process_player_guess


def process_player_guess_wrap(g):
    old_process(g)
    update_history()
    update_status()
    guess_entry.delete(0, tk.END)


process_player_guess = process_player_guess_wrap

old_start = start_new_game


def start_new_game_wrap():
    old_start()
    update_status()
    hint_button.config(state="normal")
    update_history()


start_new_game = start_new_game_wrap

start_new_game()
root.mainloop()
