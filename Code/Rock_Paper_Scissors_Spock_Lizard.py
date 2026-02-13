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
    """Enhanced GUI with scoreboard, history, quick buttons, and status bar."""

    def __init__(self) -> None:
        try:
            self.root = tk.Tk()
            self.root.title("Rock-Paper-Scissors-Lizard-Spock")
            self.root.geometry("420x420")
            self.root.resizable(False, False)
            self.root.eval("tk::PlaceWindow . center")

            # Persistent stats
            self.stats = {"wins": 0, "losses": 0, "ties": 0}
            self.history: list[Tuple[str, str, str]] = []

            # --- Header ---
            header = tk.Frame(self.root)
            header.pack(pady=6)
            tk.Label(header, text="Rock-Paper-Scissors-Lizard-Spock",
                     font=("Arial", 14, "bold")).pack()

            # --- Scoreboard ---
            score_frame = tk.Frame(self.root, relief="groove", bd=2)
            score_frame.pack(pady=6)
            self.score_lbl = tk.Label(score_frame, text=self._score_text(),
                                      font=("Arial", 10))
            self.score_lbl.pack(padx=10, pady=4)

            # --- Input area ---
            input_frame = tk.Frame(self.root)
            input_frame.pack(pady=6)
            tk.Label(input_frame, text="Enter your move:").pack()
            self.entry = tk.Entry(input_frame, width=20, justify="center")
            self.entry.pack()
            self.entry.focus()
            self.entry.bind("<Return>", self._on_submit)

            # --- Quick pick buttons ---
            btn_frame = tk.Frame(self.root)
            btn_frame.pack(pady=6)
            for move in Move:
                tk.Button(btn_frame, text=move.name.lower(),
                          command=lambda m=move: self._quick_move(m),
                          width=8).pack(side="left", padx=2)

            # --- Submit / Clear / History toggle ---
            ctrl_frame = tk.Frame(self.root)
            ctrl_frame.pack(pady=6)
            tk.Button(ctrl_frame, text="Submit", command=self._on_submit,
                      width=10, default="active").pack(side="left", padx=4)
            tk.Button(ctrl_frame, text="Clear", command=self._clear_entry,
                      width=8).pack(side="left", padx=4)
            self.history_btn = tk.Button(ctrl_frame, text="Show History",
                                         command=self._toggle_history, width=12)
            self.history_btn.pack(side="left", padx=4)

            # --- Result display ---
            self.result_lbl = tk.Label(self.root, text="",
                                       font=("Arial", 11, "italic"), fg="blue")
            self.result_lbl.pack(pady=6)

            # --- History list (hidden by default) ---
            self.history_shown = False
            self.history_frame = tk.Frame(self.root)
            self.history_listbox = tk.Listbox(self.history_frame, height=6, width=50)
            scrollbar = tk.Scrollbar(self.history_frame, orient="vertical")
            scrollbar.config(command=self.history_listbox.yview)
            self.history_listbox.config(yscrollcommand=scrollbar.set)
            self.history_listbox.pack(side="left", fill="y")
            scrollbar.pack(side="right", fill="y")

            # --- Status bar ---
            self.status = tk.Label(self.root, text="Ready", bd=1, relief="sunken",
                                   anchor="w", font=("Arial", 8))
            self.status.pack(side="bottom", fill="x")

        except Exception as e:
            print(f"Error initializing GUI: {e}")
            raise

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------
    def _score_text(self) -> str:
        return f"Wins: {self.stats['wins']}   Losses: {self.stats['losses']}   Ties: {self.stats['ties']}"

    def _update_status(self, msg: str) -> None:
        self.status.config(text=msg)
        self.root.update_idletasks()

    def _clear_entry(self) -> None:
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def _quick_move(self, move: Move) -> None:
        self.entry.delete(0, tk.END)
        self.entry.insert(0, move.name.lower())
        self._on_submit()

    def _toggle_history(self) -> None:
        if self.history_shown:
            self.history_frame.pack_forget()
            self.history_btn.config(text="Show History")
            self.history_shown = False
        else:
            self.history_frame.pack(pady=6)
            self.history_btn.config(text="Hide History")
            self.history_shown = True

    def _on_submit(self, _event=None) -> None:
        """Handle submit button click or Enter key press."""
        raw = self.entry.get().strip()
        if not raw:
            self._update_status("Please enter a move.")
            return

        try:
            player = Move.from_str(raw)
        except ValueError as e:
            self._update_status(str(e))
            return

        player_move, computer_move, result = play(player)
        self._record_result(player_move, computer_move, result)

        # Update GUI
        self.result_lbl.config(
            text=f"You: {player_move.name.lower()}  |  "
                 f"Computer: {computer_move.name.lower()}  |  {result}"
        )
        self.score_lbl.config(text=self._score_text())
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self._update_status("Round complete.")

    def _record_result(self, player: Move, computer: Move, result: str) -> None:
        """Update stats and history."""
        if "win" in result.lower():
            self.stats["wins"] += 1
        elif "lose" in result.lower():
            self.stats["losses"] += 1
        else:
            self.stats["ties"] += 1

        self.history.append((player.name, computer.name, result))
        self.history_listbox.insert(
            tk.END,
            f"{player.name.lower()} vs {computer.name.lower()} -> {result}"
        )
        self.history_listbox.see(tk.END)

    def run(self) -> None:
        """Start the GUI event loop."""
        self.root.mainloop()

# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------


if __name__ == "__main__":
    try:
        RPSLSGui().run()
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl-C in terminal
        print("\nGame terminated.")
