# template for "Stopwatch: The Game"

#-------------------------------------------------
#-------------------------------------------------

# global state

import tkinter as tk


# define global variables
ticks = 0
total_stops = 0
correct_stops = 0

timer_stopped = True

#-------------------------------------------------
#-------------------------------------------------

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    
    # one tenth of a second
    d = t % 10
    
    # total seconds
    seconds = t // 10

    a = seconds // 60
    
    bc = seconds % 60
    
    c = bc % 10
    b = bc // 10
    
    
    result = str(a) + ":" + str(b) + str(c) + "." + str(d)
    
    return result
    
#-------------------------------------------------    
#-------------------------------------------------

    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    global timer_stopped
    timer.start()
    timer_stopped = False

    
def stop():
    global timer_stopped
    
    if not timer_stopped:
        timer.stop()

        global total_stops, correct_stops

        if ticks % 10 == 0:
            correct_stops += 1

        total_stops += 1
        
        timer_stopped = True
    

def reset():
    global ticks, correct_stops, total_stops, timer_stopped
    ticks = 0
    correct_stops = 0
    total_stops = 0
    timer_stopped = True
    timer.stop()
    update_display()


# define event handler for timer with 0.1 sec interval
def increment_ticks():
    global ticks
    ticks += 1
    update_display()


# define draw handler
def update_display():
    time_text = format(ticks)
    score_text = f"{correct_stops}/{total_stops}"
    canvas.itemconfig(time_item, text=time_text)
    canvas.itemconfig(score_item, text=score_text)


#-------------------------------------------------    
#-------------------------------------------------
    
    
# create frame
root = tk.Tk()
root.title("Stop Watch: The Game")
root.resizable(False, False)

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

time_item = canvas.create_text(75, 100, text=format(ticks), fill="Green",
                               font=("Helvetica", 40), anchor="w")
score_item = canvas.create_text(270, 20, text=f"{correct_stops}/{total_stops}",
                                fill="Red", font=("Helvetica", 20), anchor="ne")

# Timer using after loop
timer_id = None

def timer_start():
    global timer_id
    if timer_id is None:
        increment_ticks()
        timer_id = root.after(100, timer_start)

def timer_stop():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

timer = type('Timer', (), {'start': timer_start, 'stop': timer_stop})()

#-------------------------------------------------    
#-------------------------------------------------


# register event handlers
button_frame = tk.Frame(root)
button_frame.pack()

start_btn = tk.Button(button_frame, text="Start", command=start, width=10)
start_btn.pack(side="left", padx=5, pady=5)

stop_btn = tk.Button(button_frame, text="Stop", command=stop, width=10)
stop_btn.pack(side="left", padx=5, pady=5)

reset_btn = tk.Button(button_frame, text="Reset", command=reset, width=10)
reset_btn.pack(side="left", padx=5, pady=5)


#-------------------------------------------------    
#-------------------------------------------------

# start frame
root.mainloop()


#-------------------------------------------------    
#-------------------------------------------------
