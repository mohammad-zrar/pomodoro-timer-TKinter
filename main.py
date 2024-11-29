from tkinter import *
from math import floor
import os
import sys

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#F5F2C7"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECKMARK = "✔"
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    check_mark_label.config(text="")
    title_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def timer_start():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = "0" + str(count_sec)
    if count_min < 10:
        count_min = "0" + str(count_min)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        timer_start()
        if reps % 2 == 0:
            check_mark = CHECKMARK * int(reps / 2)
            check_mark_label.config(text=check_mark)

# ---------------------------- UI SETUP ------------------------------- #
def resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

window.resizable(False, False)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# tomato_img = PhotoImage(file="tomato.png")
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 32, "bold"))
canvas.grid(column=1, row=1)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 45, "bold"))
title_label.grid(column=1, row=0)

start_button = Button(text="Start", border=2.5, highlightthickness=2.5, command=timer_start)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", border=2.5, highlightthickness=2.5, command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 16, "italic"))
check_mark_label.grid(column=1, row=3)

window.mainloop()
