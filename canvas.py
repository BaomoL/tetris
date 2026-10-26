import sys, os, time

class Canvas:

    # define the canvas to be drawn on by height and width
    # tiles are represented by tuples that include a character, background color, and foreground color
    # default (' ', None, None) meaning blank space with no color

    def __init__(self, width, height):

        size = os.get_terminal_size()

        if size.columns < width or size.lines < height:
            print('please make screen bigger')

            while size.columns < width or size.lines < height:
                size = os.get_terminal_size()
                time.sleep(0.1)

        sys.stdout.write('\033[?1049h\033[2J\033[H\033[?25l')

        self.width = width
        self.height = height
        self.buffer = [[(' ', None, None) for _ in range(width)] for _ in range(height)]

        self.load(self.buffer)

    def rectangle(self, x, y, width, height, color = None):

        for i in range(1, width + 1):
            for j in range(1, height + 1):
                self.single_rectangle(x + i -1, y + j - 1, color)

    def char(self, x, y, text, fcolor = None, bcolor = None):

        fg = f'\033[38;2;{fcolor[0]};{fcolor[1]};{fcolor[2]}m' if fcolor else '\033[39m'
        bg = f'\033[48;2;{bcolor[0]};{bcolor[1]};{bcolor[2]}m' if bcolor else '\033[49m'
        sys.stdout.write(f'\033[{y};{x}H{fg}{bg}{text}\033[0m')
    
    # compares the canvas with previous and makes changes only to updated tiles

    def load(self, new_canvas):
        for row in range(len(self.buffer)):
            for column in range(len(self.buffer[row])):
                if self.buffer[row][column] != new_canvas[row][column]:
                    self.char(column+1, row+1, *new_canvas[row][column])
        self.buffer = [row[:] for row in new_canvas]

        sys.stdout.flush()

        # returns current canvas    

    def get_canvas(self):
        return [row[:] for row in self.buffer]

    # makes a default blank canvas

    def blank_canvas(self):
        return [[(' ', None, None) for _ in range(self.width)] for _ in range(self.height)]
        
    def close(self):
        sys.stdout.write('\033[0m\033[?25h\033[?1049l')
        sys.stdout.flush()