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

# Global game-state variables
elapsed_tenths = 0        # time elapsed in tenths of seconds
total_attempts = 0        # how many times the user pressed Stop
successful_attempts = 0   # how many stops landed on a whole second
timer_is_paused = True    # flag indicating if the timer is currently paused

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

# =============================================================================
#  3. Event Handlers for Buttons (Start, Stop, Reset)
# =============================================================================

def start_timer() -> None:
    """Start the stopwatch timer and set the paused flag to False."""
    global timer_is_paused
    stopwatch_timer.start()
    timer_is_paused = False


def stop_timer() -> None:
    """
    Stop the stopwatch timer if it is running.
    Increment total attempts and, if stopped on a whole second,
    increment successful attempts.
    """
    global timer_is_paused, total_attempts, successful_attempts

    if not timer_is_paused:
        stopwatch_timer.stop()
        if elapsed_tenths % 10 == 0:
            successful_attempts += 1
        total_attempts += 1
        timer_is_paused = True


def reset_timer() -> None:
    """Reset all game state and stop the timer."""
    global elapsed_tenths, successful_attempts, total_attempts, timer_is_paused
    elapsed_tenths = successful_attempts = total_attempts = 0
    timer_is_paused = True
    stopwatch_timer.stop()
    refresh_display()


# =============================================================================
#  4. Timer & Display Handlers
# =============================================================================

def increment_elapsed() -> None:
    """Increment elapsed time by one tenth of a second and refresh display."""
    global elapsed_tenths
    elapsed_tenths += 1
    refresh_display()


def refresh_display() -> None:
    """Update the canvas text items for time and score."""
    canvas.itemconfig(time_display, text=format_time(elapsed_tenths))
    canvas.itemconfig(score_display, text=f"{successful_attempts}/{total_attempts}")

# =============================================================================
#  5. GUI Setup – Main Window & Canvas
# =============================================================================

root = tk.Tk()
root.title("Stop Watch: The Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

time_display = canvas.create_text(
    75, 100,
    text=format_time(elapsed_tenths),
    fill="Green",
    font=("Helvetica", 40),
    anchor="w"
)

score_display = canvas.create_text(
    270, 20,
    text=f"{successful_attempts}/{total_attempts}",
    fill="Red",
    font=("Helvetica", 20),
    anchor="ne"
)

# =============================================================================
#  6. Timer Implementation using tkinter's after() loop
# =============================================================================

timer_id = None  # Holds the after() ID to allow cancellation


def timer_start() -> None:
    """Start the after() loop that increments elapsed time every 100 ms."""
    global timer_id
    if timer_id is None:
        increment_elapsed()
        timer_id = root.after(100, timer_start)


def timer_stop() -> None:
    """Cancel the after() loop, effectively pausing the timer."""
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None


# Create a simple object with start/stop methods for consistent interface
stopwatch_timer = type('Timer', (), {'start': timer_start, 'stop': timer_stop})()

# =============================================================================
#  7. Buttons & Event Binding
# =============================================================================

button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start", command=start_timer, width=10)
start_button.pack(side="left", padx=5, pady=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_timer, width=10)
stop_button.pack(side="left", padx=5, pady=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_timer, width=10)
reset_button.pack(side="left", padx=5, pady=5)

# =============================================================================
#  8. Run Application
# =============================================================================

root.mainloop()
