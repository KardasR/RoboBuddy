from curses import wrapper
import curses
from time import sleep


#curses.noecho()     # makes key presses not show in terminal
#curses.cbreak()     # take in input without needing to press enter

def close():
    curses.echo()
    curses.nocbreak()
    exit(0)

def drawCursesBox():
    def start(screen):
        screen = curses.initscr()
        screen.clear()
        
        screen.border()
        print(screen.getmaxyx())

        screen.refresh()

        val = screen.getch()

        if (val == 120): # x key
            close()

    wrapper(start)

while(True):
    drawCursesBox()