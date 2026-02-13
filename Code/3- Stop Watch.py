# =============================================================================
#  Stopwatch: The Game – Sectioned Template
# =============================================================================
#  A simple stopwatch game implemented with tkinter. The goal is to stop the
#  timer right on a whole second (tenths digit == 0). Score is displayed as
#  successful_stops / total_stops.
# =============================================================================

# =============================================================================
#  1. Imports & Global State
# =============================================================================

import tkinter as tk
from tkinter import ttk
from typing import Tuple
import threading
import time

# Global game-state variables
_elapsed_tenths = 0        # time elapsed in tenths of seconds
_total_attempts = 0        # how many times the user pressed Stop
_successful_attempts = 0   # how many stops landed on a whole second
_timer_is_paused = True    # flag indicating if the timer is currently paused
_state_lock = threading.Lock()  # Lock to protect concurrent access
_MAX_ATTEMPTS = 5          # maximum attempts allowed before forced reset

# =============================================================================
#  2. Helper Functions
# =============================================================================

def format_time(tenths: int) -> str:
    """
    Convert time expressed in tenths of seconds to a formatted string A:BC.D.

    Parameters
    ----------
    tenths : int
        Total time elapsed in tenths of seconds.

    Returns
    -------
    str
        Formatted time string as minutes:seconds.tenths
    """
    tenths_digit = tenths % 10
    total_seconds = tenths // 10
    minutes, remaining_seconds = divmod(total_seconds, 60)
    seconds_tens, seconds_ones = divmod(remaining_seconds, 10)
    return f"{minutes}:{seconds_tens}{seconds_ones}.{tenths_digit}"


def get_score_text() -> str:
    """Return the current score string."""
    with _state_lock:
        return f"{_successful_attempts}/{_total_attempts}"


def is_on_whole_second() -> bool:
    """Check if the current elapsed time is on a whole second."""
    with _state_lock:
        return _elapsed_tenths % 10 == 0


def reset_game_state() -> None:
    """Reset all game-state variables to initial values."""
    global _elapsed_tenths, _successful_attempts, _total_attempts, _timer_is_paused
    with _state_lock:
        _elapsed_tenths = _successful_attempts = _total_attempts = 0
        _timer_is_paused = True


def get_accuracy_percentage() -> float:
    """Return the accuracy as a percentage (0-100)."""
    with _state_lock:
        return (_successful_attempts / _total_attempts * 100) if _total_attempts else 0.0


def get_accuracy_color(percentage: float) -> str:
    """Return a color string based on accuracy percentage."""
    if percentage >= 80:
        return "green"
    elif percentage >= 50:
        return "orange"
    else:
        return "red"

# =============================================================================
#  3. Event Handlers for Buttons (Start, Stop, Reset)
# =============================================================================

def start_timer() -> None:
    """Start the stopwatch timer and set the paused flag to False."""
    global _timer_is_paused
    with _state_lock:
        if not _timer_is_paused:
            return  # Prevent double-start
        if _total_attempts >= _MAX_ATTEMPTS:
            return  # Do not allow starting if max attempts reached
        _timer_is_paused = False
    stopwatch_timer.start()


def stop_timer(*args) -> None:
    """
    Stop the stopwatch timer if it is running.
    Increment total attempts and, if stopped on a whole second,
    increment successful attempts.
    """
    global _timer_is_paused, _total_attempts, _successful_attempts
    with _state_lock:
        if _timer_is_paused:
            return  # Prevent stop when already paused
        _timer_is_paused = True
        if is_on_whole_second():
            _successful_attempts += 1
        _total_attempts += 1
    stopwatch_timer.stop()
    refresh_display()
    show_accuracy_popup()
    # Force reset if max attempts reached
    if _total_attempts >= _MAX_ATTEMPTS:
        root.after(1000, reset_timer)


def reset_timer(*args) -> None:
    """Reset all game state and stop the timer."""
    reset_game_state()
    stopwatch_timer.stop()
    refresh_display()


# =============================================================================
#  4. Timer & Display Handlers
# =============================================================================

def increment_elapsed() -> None:
    """Increment elapsed time by one tenth of a second and refresh display."""
    global _elapsed_tenths
    with _state_lock:
        _elapsed_tenths += 1
    refresh_display()


def refresh_display() -> None:
    """Update the canvas text items for time and score."""
    with _state_lock:
        time_text = format_time(_elapsed_tenths)
        score_text = get_score_text()
        acc = get_accuracy_percentage()
        color = get_accuracy_color(acc)
        acc_text = f"{acc:.1f}%"
    canvas.itemconfig(time_display, text=time_text)
    canvas.itemconfig(score_display, text=score_text)
    canvas.itemconfig(accuracy_display, text=acc_text, fill=color)
    # Update attempts progress bar
    attempts_progress["value"] = _total_attempts
    attempts_label.config(text=f"Attempts: {_total_attempts}/{_MAX_ATTEMPTS}")


def show_accuracy_popup() -> None:
    """Show a small transient popup with the latest accuracy."""
    acc = get_accuracy_percentage()
    color = get_accuracy_color(acc)
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    # Clamp position to stay within screen bounds
    x = max(0, min(root.winfo_x() + 350, root.winfo_screenwidth() - 100))
    y = max(0, min(root.winfo_y() + 100, root.winfo_screenheight() - 100))
    popup.geometry(f"+{x}+{y}")
    label = tk.Label(popup, text=f"{acc:.1f}%", fg=color, font=("Helvetica", 24))
    label.pack(padx=20, pady=10)
    root.after(1000, popup.destroy)


# =============================================================================
#  5. GUI Setup – Main Window & Canvas
# =============================================================================

root = tk.Tk()
root.title("Stop Watch: The Game")
root.resizable(False, False)

# Set window on top and remove full-screen to reduce attack surface
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW", root.quit)

# Main frame to hold canvas and controls
main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10)

canvas = tk.Canvas(main_frame, width=400, height=200, bg="white", relief="ridge", bd=2)
canvas.pack()

time_display = canvas.create_text(
    200, 100,
    text=format_time(0),
    fill="Green",
    font=("Helvetica", 48, "bold"),
    anchor="center"
)

score_display = canvas.create_text(
    350, 30,
    text=get_score_text(),
    fill="Red",
    font=("Helvetica", 24),
    anchor="ne"
)

accuracy_display = canvas.create_text(
    350, 60,
    text="0.0%",
    fill="gray",
    font=("Helvetica", 18),
    anchor="ne"
)

# =============================================================================
#  6. Timer Implementation using tkinter's after() loop
# =============================================================================

_timer_id = None  # Holds the after() ID to allow cancellation


def timer_start() -> None:
    """Start the after() loop that increments elapsed time every 100 ms."""
    global _timer_id
    if _timer_id is not None:
        return
    increment_elapsed()
    _timer_id = root.after(100, timer_start)


def timer_stop() -> None:
    """Cancel the after() loop, effectively pausing the timer."""
    global _timer_id
    if _timer_id is not None:
        root.after_cancel(_timer_id)
        _timer_id = None


# Create a simple object with start/stop methods for consistent interface
stopwatch_timer = type('Timer', (), {'start': timer_start, 'stop': timer_stop})()

# =============================================================================
#  7. Buttons & Event Binding
# =============================================================================

# Controls frame
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(fill="x", pady=(10, 0))

# Attempts progress bar and label
attempts_frame = ttk.Frame(controls_frame)
attempts_frame.pack(fill="x", pady=(0, 10))

attempts_label = ttk.Label(attempts_frame, text=f"Attempts: 0/{_MAX_ATTEMPTS}", font=("Helvetica", 14))
attempts_label.pack(side="left")

attempts_progress = ttk.Progressbar(attempts_frame, maximum=_MAX_ATTEMPTS, length=200)
attempts_progress.pack(side="right", padx=(10, 0))

# Buttons frame
button_frame = ttk.Frame(controls_frame)
button_frame.pack()

start_button = ttk.Button(button_frame, text="Start", command=start_timer, width=12)
start_button.pack(side="left", padx=5)

stop_button = ttk.Button(button_frame, text="Stop", command=stop_timer, width=12)
stop_button.pack(side="left", padx=5)

reset_button = ttk.Button(button_frame, text="Reset", command=reset_timer, width=12)
reset_button.pack(side="left", padx=5)

# =============================================================================
#  8. Keyboard shortcuts
# =============================================================================

# Use root.bind_all to ensure no widget overrides these bindings
root.bind_all("<space>", lambda e: start_timer() if _timer_is_paused and _total_attempts < _MAX_ATTEMPTS else (stop_timer() if not _timer_is_paused else None))
root.bind_all("<r>", lambda e: reset_timer())

# =============================================================================
#  9. Run Application
# =============================================================================

if __name__ == "__main__":
    root.mainloop()
