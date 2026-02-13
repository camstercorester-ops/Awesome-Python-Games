# template for "Stopwatch: The Game"

#-------------------------------------------------
#-------------------------------------------------

# global state

import tkinter as tk


# define global variables
elapsed_tenths = 0
total_attempts = 0
successful_attempts = 0

timer_is_paused = True

#-------------------------------------------------
#-------------------------------------------------

# define helper function format_time that converts time
# in tenths of seconds into formatted string A:BC.D
def format_time(tenths):
    
    # one tenth of a second
    tenths_digit = tenths % 10
    
    # total seconds
    total_seconds = tenths // 10

    minutes = total_seconds // 60
    
    remaining_seconds = total_seconds % 60
    
    seconds_ones = remaining_seconds % 10
    seconds_tens = remaining_seconds // 10
    
    
    formatted_time = str(minutes) + ":" + str(seconds_tens) + str(seconds_ones) + "." + str(tenths_digit)
    
    return formatted_time
    
#-------------------------------------------------    
#-------------------------------------------------

    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start_timer():
    global timer_is_paused
    stopwatch_timer.start()
    timer_is_paused = False

    
def stop_timer():
    global timer_is_paused
    
    if not timer_is_paused:
        stopwatch_timer.stop()

        global total_attempts, successful_attempts

        if elapsed_tenths % 10 == 0:
            successful_attempts += 1

        total_attempts += 1
        
        timer_is_paused = True
    

def reset_timer():
    global elapsed_tenths, successful_attempts, total_attempts, timer_is_paused
    elapsed_tenths = 0
    successful_attempts = 0
    total_attempts = 0
    timer_is_paused = True
    stopwatch_timer.stop()
    refresh_display()


# define event handler for timer with 0.1 sec interval
def increment_elapsed():
    global elapsed_tenths
    elapsed_tenths += 1
    refresh_display()


# define draw handler
def refresh_display():
    time_text = format_time(elapsed_tenths)
    score_text = f"{successful_attempts}/{total_attempts}"
    canvas.itemconfig(time_display, text=time_text)
    canvas.itemconfig(score_display, text=score_text)


#-------------------------------------------------    
#-------------------------------------------------
    
    
# create frame
root = tk.Tk()
root.title("Stop Watch: The Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

time_display = canvas.create_text(75, 100, text=format_time(elapsed_tenths), fill="Green",
                               font=("Helvetica", 40), anchor="w")
score_display = canvas.create_text(270, 20, text=f"{successful_attempts}/{total_attempts}",
                                fill="Red", font=("Helvetica", 20), anchor="ne")

# Timer using after loop
timer_id = None

def timer_start():
    global timer_id
    if timer_id is None:
        increment_elapsed()
        timer_id = root.after(100, timer_start)

def timer_stop():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

stopwatch_timer = type('Timer', (), {'start': timer_start, 'stop': timer_stop})()

#-------------------------------------------------    
#-------------------------------------------------


# register event handlers
button_frame = tk.Frame(root)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start", command=start_timer, width=10)
start_button.pack(side="left", padx=5, pady=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_timer, width=10)
stop_button.pack(side="left", padx=5, pady=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_timer, width=10)
reset_button.pack(side="left", padx=5, pady=5)


#-------------------------------------------------    
#-------------------------------------------------

# start frame
root.mainloop()


#-------------------------------------------------    
#-------------------------------------------------
