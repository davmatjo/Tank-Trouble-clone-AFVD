from math import sin
from math import cos
from math import radians
from math import degrees


def degsin(x):
    x = radians(x)
    answer = sin(x)
    return answer


def degcos(x):
    x = radians(x)
    answer = cos(x)
    return answer
