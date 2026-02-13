"""
Rock-Paper-Scissors-Lizard-Spock
A fast, type-safe implementation of the classic expanded RPS game.
"""

from __future__ import annotations
import random
import tkinter as tk
from enum import IntEnum, unique
from typing import Final, Tuple

# ------------------------------------------------------------------
# Domain model
# ------------------------------------------------------------------

@unique
class Move(IntEnum):
    """Strongly-typed moves with built-in conversion."""
    ROCK = 0
    SPOCK = 1
    PAPER = 2
    LIZARD = 3
    SCISSORS = 4

    @classmethod
    def from_str(cls, name: str) -> "Move":
        """Case-insensitive conversion from string."""
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"Invalid move: {name!r}") from None

    def beats(self, other: "Move") -> int:
        """
        Return:
            1  if self wins
            0  if tie
            -1 if self loses
        """
        diff = (self - other) % 5
        if diff == 0:
            return 0
        return 1 if diff in {1, 2} else -1

# ------------------------------------------------------------------
# Game engine
# ------------------------------------------------------------------


_RESULT_MAP: Final[Tuple[str, str, str]] = ("Tie!", "Player wins!", "Computer wins!")


def play(player_move: Move) -> Tuple[Move, Move, str]:
    """Run one round and return (player, computer, result_text)."""
    computer_move = Move(random.randrange(5))
    outcome = player_move.beats(computer_move)
    return player_move, computer_move, _RESULT_MAP[outcome]

# ------------------------------------------------------------------
# CLI helper
# ------------------------------------------------------------------


def rpsls(player_choice: str) -> Tuple[Move, Move, str] | None:
    """CLI-friendly wrapper; prints result and returns data or None on error."""
    try:
        player = Move.from_str(player_choice)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    player_move, computer_move, result = play(player)
    print("-" * 20)
    print(f"Player chooses   : {player_move.name.lower()}")
    print(f"Computer chooses : {computer_move.name.lower()}")
    print(result)
    return player_move, computer_move, result

# ------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------


class RPSLSGui:
    """Lightweight GUI with inline styling."""

    def __init__(self) -> None:
        try:
            self.root = tk.Tk()
            self.root.title("Rock-Paper-Scissors-Lizard-Spock")
            self.root.geometry("320x160")
            self.root.resizable(False, False)
            self.root.eval("tk::PlaceWindow . center")

            tk.Label(self.root, text="Enter your move:").pack(pady=(10, 0))
            self.entry = tk.Entry(self.root, width=18, justify="center")
        except Exception as e:
            print(f"Error initializing GUI: {e}")
            raise
        self.entry.pack()          
        self.entry.focus()
        self.entry.bind("<Return>", self._on_submit)

        tk.Button(self.root, text="Submit", command=self._on_submit, width=10).pack(pady=6)

        tk.Label(self.root,
                 text="Valid: rock, paper, scissors, lizard, spock",
                 font=("Arial", 8), fg="grey").pack(pady=(0, 10))

    def _on_submit(self, _event=None) -> None:
        """Handle submit button click or Enter key press."""
        player_move = rpsls(self.entry.get())
        if player_move is None:
            return
        # Clear entry field after submission
        self.entry.delete(0, tk.END)

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()
        # Clean up on close
        self.root.destroy()

# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    try:
        RPSLSGui().run()
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl-C in terminal
        pass
        print("\nGame terminated.")