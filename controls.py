from config import (rotate_clockwise, rotate_counter_clockwise, rotate_one_eighty, rotate_clockwise_backup,
                    move_left, move_right, soft_drop, hard_drop, hold)

from enum import Enum, auto
from keys import pressed
from pynput.keyboard import Key

class Action(Enum):
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    ROTATE_180 = auto()
    LEFT = auto()
    RIGHT = auto()
    SOFT_DROP = auto()
    HARD_DROP = auto()
    HOLD = auto()
    MENU_DOWN = auto()
    MENU_UP = auto()
    MENU_RIGHT = auto()
    MENU_LEFT = auto()
    MENU_ENTER = auto()


keybinds = {'game': 
            {rotate_clockwise: Action.ROTATE_CW,
            rotate_counter_clockwise: Action.ROTATE_CCW, 
            rotate_one_eighty: Action.ROTATE_180, 
            rotate_clockwise_backup: Action.ROTATE_CW,
            move_left: Action.LEFT, 
            move_right: Action.RIGHT, 
            soft_drop: Action.SOFT_DROP, 
            hard_drop: Action.HARD_DROP, 
            hold: Action.HOLD
            },

            'menu':
            {Key.up: Action.MENU_UP,
            Key.down: Action.MENU_DOWN,
            Key.left: Action.MENU_LEFT,
            Key.right: Action.MENU_RIGHT,
            Key.enter: Action.MENU_ENTER
            }}

class Controls:

    def __init__(self, game_state):
        self.last_held = set(pressed)
        self.game_state = game_state

    def read(self):

        keys_pressed = set(pressed)

        held_actions = set()

        for key in keys_pressed:
            action = keybinds[self.game_state].get(key)
            if action is not None:
                held_actions.add(action)

        new_actions = held_actions - self.last_held

        self.last_held = held_actions


        return new_actions, held_actions