import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Typing speed test!")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.refresh()
    stdscr.getkey()

def display_test(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1,0, f"WPM: {wpm}")


    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        
        stdscr.addstr(0,i, char, color)
        stdscr.nodelay(True) #changes the .getkey() to non-blocking statement

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choise(lines).strip()   #strip removes white space char (\n)

def wpm_test(stdscr):
    target_text = "Hello World! this is a sample text for this app"
    current_text = []  #list of keys

    wpm = 0

    start_time = time.time()
    

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) #char/min divided by 5 is wpm

        stdscr.clear()
        display_test(stdscr, target_text, current_text, wpm)
        stdscr.refresh()
        

        #check whether the entire target_text is typed
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()   #waits for the key here
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()

        # elif key in ("KEY_DELETE"):
        #     if len(current_text) > 0:
        #         current_text. 
        elif len(current_text) < len(target_text):
            current_text.append(key) 

        
        

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    
    while True:
        wpm_test(stdscr)

        stdscr.addstr(3, 1, "You completed the text! \nPress any key to continue")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)