import sys, time
from terminal import raw_mode
from pynput.keyboard import Key
from game import Game
from keys import pressed, listener
from canvas import Canvas
from renderer import display_menu
from controls import Controls, Action
from config import (rotate_clockwise, rotate_counter_clockwise, rotate_one_eighty, rotate_clockwise_backup,
                    move_left, move_right, soft_drop, hard_drop, hold)


page = {
    "Marathon": ("Marathon",),

    "Sprint": {
        "20 Lines": ("Sprint", 20),
        "40 Lines": ("Sprint", 40),
        "100 Lines": ("Sprint", 100),
    },

    "Ultra": {
        "1 Minute": ("Ultra", None, 60),
        "2 Minutes": ("Ultra", None, 120),
        "5 Minutes": ("Ultra", None, 300),
    },

    "Hardcore": ("Hardcore",),

    "Settings": {
        "Move Left": move_left,
        "Move Right": move_right,
        "Soft Drop": soft_drop,
        "Hard Drop": hard_drop,
        "Hold": hold,
        "Rotate Clockwise": rotate_clockwise,
        "Rotate Counter-Clockwise": rotate_counter_clockwise,
        "Rotate 180": rotate_one_eighty,
        "Rotate Clockwise (Backup)": rotate_clockwise_backup,
    },

    "Start": True
}

game_canvas = Canvas(50, 35)
input = Controls('menu')
game_mode = None
selected = 0
stack = [(page, "Select Mode")]
current = stack[-1][0]
options = list(current)
entered = {"Ultra": (("Ultra", None, 120), 1), "Sprint": (("Sprint", 40, None), 1)}
start = False

with raw_mode():
    try:
        listener.start()

        while not start:

            new_actions, held_actions = input.read()

            if Action.MENU_DOWN in new_actions:
                selected = (selected +1) % len(options)

            if Action.MENU_UP in new_actions:
                selected = (selected - 1) % len(options)

            if Action.MENU_RIGHT in new_actions:
                value = current[options[selected]]
                if isinstance(value, dict):
                    stack.append((value, options[selected]))
                    if selected >= len(list(value)):
                        selected = len(list(value)) -1

            if Action.MENU_LEFT in new_actions:
                if len(stack)>1:
                    stack.pop()
                current = stack[-1][0]
                if selected >= len(list(current)):
                    selected = len(list(current)) - 1

            current = stack[-1][0]
            current_title = stack[-1][1]
            options = list(current)

            if Action.MENU_ENTER in new_actions:
                value = current[options[selected]]
                if not isinstance(value, dict):
                    entered[current_title] = (value, selected)
                if options[selected] in ("Marathon", "Sprint", "Ultra", "Hardcore"):
                    game_mode = options[selected]
                if options[selected] == "Start":
                    start = True
                

            display_menu(game_canvas, selected, current_title, options, entered, game_mode)

            time.sleep(0.01)
        if game_mode in ("Sprint", "Ultra"):
            game_mode = entered[game_mode][0]
        else:
            game_mode = (game_mode,)
        game = Game(game_canvas, *game_mode)
        game.start()

    finally:

        listener.stop()

