import curses
from curses import wrapper
import time
import random

# Displays the start or welcome screen, prompting user to press a key to start the test
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to speed typing test!")
    stdscr.addstr("\nPress any key to proceed!")
    stdscr.refresh()
    stdscr.getkey()

# Displays the target text, dynamic words per minute and color codes user input to check for accuracy
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)                                       
    stdscr.addstr(1, 0, f"WPM: {wpm}")                          # Displays calculated words per minute below the target

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)                        # Color codes incorrect character as red        
        stdscr.addstr(0, i, char, color)

# Randomly selects a sentence from the collection of texts in tests.text
def load_text():
    with open("test.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

# Calculates dynamic words per minute
def wpm_test(stdscr):
    target_text = load_text()                                   
    current_text = []
    wpm = 0
    start_time = time.time()                                    # Gives time elapsed in seconds since the Unix epoch
    stdscr.nodelay(True)                                        # For updating wpm even when the user is idle after starting the test

    while True:
        time_elapsed = max(time.time() - start_time, 1)         # Minimum is set to one to prevent division by zero in wpm calculation
        wpm = round((len(current_text) / (time_elapsed/60))/5)  # Taking average length of word to be 5

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)                               # Stops updating wpm once user gets the correct sentence
            break

        try:                                                    # Prevents "no input" error due to nodelay(True) when the user is idle
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

# Execution of the code
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Sets the color codes to be used
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        
        if ord(key) == 27:                                      # Pressing escape key exits the test
            break

wrapper(main)
