from canvas import Canvas
from pieces import Piece

color = {
    '0': None,
    '1': (90, 96, 106),
    '2': (175, 65, 230),    # t  purple
    '3': (235, 55, 55),     # z  red
    '4': (65, 205, 75),     # s  green
    '5': (0, 220, 240),     # i  cyan
    '6': (255, 155, 25),    # l  orange
    '7': (45, 90, 235),     # j  blue
    '8': (250, 215, 35),    # o  yellow
}

offset = 10

# function for converting time to time format

def format_time(seconds):

    minutes, seconds = divmod(int(seconds), 60)

    return f'{minutes:02d}:{seconds:02d}'

# convert regular characters into blocks

def draw_block(canvas, row, col, char, offset=0):
    canvas[row][col*2 + offset] = char
    canvas[row][col*2+1 + offset] = char

# append text into canvas

def text(canvas, row, col, text, fcolor = None, bcolor = None):
        column = col
        for letter in list(text):
            canvas[row][column] = (letter, fcolor, bcolor)
            column+=1

def render(canvas, game, board):

    # current grid

    new_buffer = canvas.blank_canvas()
    for row in range(2, len(board.grid)):
        for column in range(len(board.grid[row])):
            draw_block(new_buffer, row, column, (' ', None, color[board.grid[row][column]]), 10)

    # draw piece

    for piece_y in range(len(game.active_piece.shape)):

        for piece_x in range(len(game.active_piece.shape[piece_y])):
            
            board_x = game.active_piece.x + piece_x
            board_y = game.active_piece.y + piece_y
            if game.active_piece.shape[piece_y][piece_x]:
                draw_block(new_buffer, board_y, board_x, (' ', None, game.active_piece.color), 10)

    # ghost piece
    ghost_y = game.active_piece.y

    ghost_y += board.drop_distance(game.active_piece)
        
    for y in range(len(game.active_piece.shape)):
        for x in range(len(game.active_piece.shape[y])):
            if game.active_piece.shape[y][x]:
                if board.grid[ghost_y + y][game.active_piece.x + x] not in ('1', '2', '3', '4', '5','6','7','8'):
                    draw_block(new_buffer, ghost_y+y, game.active_piece.x + x, ('░', game.active_piece.color, None), 10)

    # draw held piece

    if game.held_piece:
        piece = Piece.shapes[game.held_piece]
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    draw_block(new_buffer, 3+row, col, (' ', None, Piece.piece_colors[game.held_piece]), 0)

    # draw queue

    offset = 3

    for piece in game.pieces[:-6:-1]:
        piece_shape = Piece.shapes[piece]
        for row in range(len(piece_shape)):
            for col in range(len(piece_shape[row])):
                if piece_shape[row][col]:
                    draw_block(new_buffer, offset+row, col+18, (' ', None, Piece.piece_colors[piece]), 0)
        offset += (len(piece_shape) +1)

    text(new_buffer, 1, 2, 'HOLD', (255,255,255))
    text(new_buffer, 1, 36, 'NEXT', (255,255,255))

    if game.mode == 'Sprint':
        text(new_buffer, 23, 10, f'{game.mode} | {game.total_lines}/{game.sprint}', (255,255,255))

    if game.mode in ('Hardcore', 'Marathon'):
        text(new_buffer, 23, 10, f'{game.mode} | Level: {game.level}', (255,255,255))

    if game.mode == 'Ultra':
        text(new_buffer, 23, 10, f'{game.mode} | {format_time(game.elapsed_time)}/{format_time(game.ultra)}', (255,255,255))

    text(new_buffer, 24, 10, f'Score: {int(game.score)}', (255,255,255))
    text(new_buffer, 25, 10, f'Elapsed Time: {format_time(game.elapsed_time)}', (255,255,255))
    text(new_buffer, 26, 10, f'Combo: {game.combo}', (255,255,255))
    text(new_buffer, 27, 10, f'Placed: {board.placed_pieces}', (255,255,255))
    if game.elapsed_time > 0:
        text(new_buffer, 28, 10, f'PPS: {round(board.placed_pieces/game.elapsed_time, 2)}', (255,255,255))
    if game.last_clear_type:
        text(new_buffer, 29, 10, game.last_clear_type, (255,255,255))
    
    canvas.load(new_buffer)
