from math import sin
from math import cos
from math import radians
from math import degrees
from math import atan
from math import floor


def degsin(x):
    x = radians(x)
    answer = sin(x)
    return answer


def degcos(x):
    x = radians(x)
    answer = cos(x)
    return answer


def arctandeg(x, y):
    answer = atan(y/x)
    return degrees(answer)


def get_player_grid(position, maze_size, screen_size):
    grid_size = screen_size[0] / maze_size
    print(position)
    grid_ref = [floor(position[0] / grid_size), floor(position[1] / grid_size)]
    return  grid_ref

