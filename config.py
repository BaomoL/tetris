# customize your game!

from pynput.keyboard import Key

t, z, s, i ,l, j, o = None, None, None, None, None, None, None


"""Game Settings"""
das = 0.1
arr = 0.01
# use 'instant' for instant drop
soft_drop_multiplier = 'instant'
stationary_touch_time = 0.5
horizontal_touch_time = 5
absolute_time =  20

tick_rate = 200
fps = 60

"""Rotations"""
rotate_clockwise =          's'
rotate_counter_clockwise =  'a'
rotate_one_eighty =         'w'
rotate_clockwise_backup =   Key.up

"""Movement"""
move_left =     Key.left
move_right =    Key.right
soft_drop =     Key.down
hard_drop =     Key.space
hold =          Key.shift 