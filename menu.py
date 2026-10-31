import time
from terminal import raw_mode
from pynput.keyboard import Key
from game import Game
from keys import listener, pressed
from canvas import Canvas
from renderer import display_menu
from controls import Controls, Action, bindings, key_names

class Setting:

    def __init__(self, control_name):
        self.name = control_name

page = {
    'TUI Tetris': 
        {"Marathon": ("Marathon",),

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
            "Rotate C": Setting("rotate_clockwise"),
            "Rotate CC": Setting("rotate_counter_clockwise"),
            "Rotate 180": Setting("rotate_one_eighty"),
            "Move Left": Setting("move_left"),
            "Move Right": Setting("move_right"),
            "Soft Drop": Setting("soft_drop"),
            "Hard Drop": Setting("hard_drop"),
            "Hold": Setting("hold"),
            "Rotate C (Backup)": Setting("rotate_clockwise_backup"),
        },

        "Start": True}
}

game_canvas = Canvas(50, 35)
input = Controls('menu')
selected = 0
start = False

# track current page using stack
pages = [page["TUI Tetris"]]

# track current page label using stack
page_labels =["TUI Tetris"]

# chosen includes all selected choices
# default game_mode to avoid crashing

chosen = {'TUI Tetris': "Marathon"}

game_mode = ("Marathon",)

waiting_for = None

with raw_mode():
    try:
        listener.start()

        while not start:

            new_actions, held_actions = input.read()

            current_options = list(pages[-1])

            options_num = len(current_options)

            current_page_pointer = pages[-1]

            current_page_label = page_labels[-1]

            selected_option_pointer = current_page_pointer[current_options[selected]]

            selected_option_label = current_options[selected]

            if Action.MENU_DOWN in new_actions:
                selected = (selected +1) % options_num

            if Action.MENU_UP in new_actions:
                selected = (selected - 1) % options_num

            if Action.MENU_RIGHT in new_actions:
                if isinstance(selected_option_pointer, dict):
                    pages.append(selected_option_pointer)
                    selected = 0
                    page_labels.append(selected_option_label)

            if Action.MENU_LEFT in new_actions:
                if len(pages) > 1:
                    pages.pop()
                    page_labels.pop()
                    selected = 0

            if Action.MENU_ENTER in new_actions:

                # acts like left arrow if label contains more options
                if isinstance(selected_option_pointer, dict):
                    pages.append(selected_option_pointer)
                    selected = 0
                    page_labels.append(selected_option_label)

                if isinstance(selected_option_pointer, tuple):
                    # put selected option into dictionary
                    chosen[current_page_label] = selected_option_label

                    # tuple = game_mode
                    game_mode = selected_option_pointer
                    if current_page_label != "TUI Tetris":
                        chosen["TUI Tetris"] = current_page_label

                if isinstance(selected_option_pointer, Setting):
                    waiting_for = selected_option_pointer.name
        
                # start game
                if selected_option_label == "Start":
                    start = True

            if Action.MENU_ESC in new_actions:
                break

            lines = []

            for line in current_options:

                line_pointer = current_page_pointer[line]
                if isinstance(line_pointer, Setting):
                    if line_pointer.name == waiting_for:
                        lines.append((f'{line:<20} Press a key', True))
                    else:
                        # either show keybind name or show keybind
                        key = bindings[line_pointer.name]
                        lines.append((f'{line:<20} {key_names[key] if key in key_names else key}', False))
                else:
                    lines.append((line, line in chosen.values()))
                
            display_menu(game_canvas, lines, current_page_label, selected)

            # get last held keys
            last_held = set(pressed)

            while waiting_for:

                # look for new keys
                new_key = set(pressed) - last_held

                if new_key:
                    if list(new_key)[0] == Key.esc:
                        waiting_for = None
                        break
                    else:
                        bindings[waiting_for] = list(new_key)[0]
                        waiting_for = None
                        break
                time.sleep(0.01)
                    
 
            time.sleep(0.01)

        game = Game(game_canvas, *game_mode)
        game.start()

    finally:

        listener.stop()

