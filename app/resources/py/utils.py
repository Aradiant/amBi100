from os import fspath
from pathlib import Path
from time import time

def clamp(n, smallest, largest):
    '''Clamp number in range [smallest, largest]'''
    return max(smallest, min(n, largest))

def lerp(x, dest, scale: float, isFloat=True):
    '''Linearly interpolate a number with given scale'''
    res = x + (dest - x) * scale
    if not isFloat:
        return round(res)
    return res

def rpath(obj):
    '''Return absolute path, given a relative path'''
    return fspath(Path(__file__).parent.parent.parent / obj)

def brighten(color):
    '''Make RGB color components 255, if above 0'''
    return ([0, 255][bool(color[0])], [0, 255][bool(color[1])], [0, 255][bool(color[2])])

def now():
    '''Get amount of seconds since the epoch'''
    return time()