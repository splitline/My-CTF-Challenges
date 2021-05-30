#!/usr/bin/env python3

import curses
import sys

KEY = '2025830455298'
FLAG = "  AIS3{H1n4m1z4w4_Sh0k0gun}  "


def main(stdscr):
    try_index = 0
    LIGHT_GRAY = 70
    GRAY = 50
    DARK_GRAY = 20

    ERROR = 1
    NORMAL = 2
    DISABLED_TEXT = 3
    BUTTON_PRESSED = 4
    SUCCESS = 5
    LOCK_PANEL = 6
    BUTTON = 7
    curses.init_color(LIGHT_GRAY, 700, 700, 700)
    curses.init_color(GRAY, 500, 500, 500)
    curses.init_color(DARK_GRAY, 200, 200, 200)
    curses.init_pair(ERROR, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(DISABLED_TEXT, 50, curses.COLOR_BLACK)
    curses.init_pair(BUTTON, curses.COLOR_BLACK, LIGHT_GRAY)
    curses.init_pair(BUTTON_PRESSED, curses.COLOR_WHITE, DARK_GRAY)
    curses.init_pair(SUCCESS, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(LOCK_PANEL, curses.COLOR_BLACK, GRAY)
    stdscr.clear()

    origin_x, origin_y = 8, 2
    lock_panel = curses.newwin(22, 35, origin_y, origin_x)
    lock_panel.border('|', '|', '-', '-', 'O', 'O', 'O', 'O')
    lock_panel.bkgd(' ', curses.color_pair(LOCK_PANEL))
    lock_panel.refresh()

    keys = "123456789Q0🔒"
    buttons = {}
    for i, c in enumerate(keys):
        button = curses.newwin(3, 7, origin_y+5+4*(i//3), origin_x+5+9*(i % 3))
        button.addstr(1, 3, c)
        button.overlay(lock_panel)
        button.bkgd(' ', curses.color_pair(BUTTON))
        button.refresh()
        if c != '🔒':
            buttons[c] = button

    height, width = 3, 31
    win = curses.newwin(height, width, origin_y+1, origin_x + 2)
    win.border(' ', ' ', '-', '-', '-', '-', '-', '-')
    win.overlay(lock_panel)
    cursor = 3
    win.addstr(1, cursor, "- "*13, curses.color_pair(DISABLED_TEXT))
    win.move(1, cursor)
    win.refresh()

    while True:
        ch = win.getch()
        if chr(ch) in buttons:
            buttons[chr(ch)].bkgd(' ', curses.color_pair(BUTTON_PRESSED))
            buttons[chr(ch)].refresh()
            curses.napms(100)
            buttons[chr(ch)].bkgd(' ', curses.color_pair(BUTTON))
            buttons[chr(ch)].refresh()
            if ch == ord('Q') or ch == ord('q'):
                return
            if KEY[try_index] == chr(ch):
                win.addstr(1, cursor, chr(ch) + ' ', curses.color_pair(NORMAL))
                if len(KEY) - 1 == try_index:
                    win.addstr(1, 1, FLAG, curses.color_pair(SUCCESS))
                    win.getch()
                    return
                cursor += 2
                try_index += 1
            else:
                win.addstr(1, cursor, chr(ch), curses.color_pair(ERROR))
                win.refresh()
                curses.napms(250)
                break

    win.addstr(1, 1, "="*10+"🔒LOCKED🔒"+"="*9, curses.color_pair(ERROR))
    win.move(0, 0)
    while True:
        win.getch()


if __name__ == '__main__':
    curses.wrapper(main)
