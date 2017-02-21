from math import sin, cos, radians, degrees, atan, floor


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
    grid_ref = [floor(position[0] / grid_size), floor(position[1] / grid_size)]
    return  grid_ref

