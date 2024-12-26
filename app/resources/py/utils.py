from os import fspath
from pathlib import Path
from time import time
import math

def clamp(n, smallest, largest):
    '''Clamp number in range [smallest, largest]'''
    return max(smallest, min(n, largest))

def lerp(x, dest, scale: float, isFloat=True, easing='linear'):
    '''Linearly interpolate a number with given scale and easing.
    Available easing styles:
    ease_in, ease_out, ease_in_out, linear'''

    if easing == "ease_in":
        scale = scale * scale  # Quadratic ease-in
    elif easing == "ease_out":
        scale = 1 - (1 - scale) * (1 - scale)  # Quadratic ease-out
    elif easing == "ease_in_out":
        scale = 0.5 * (1 - math.cos(scale * math.pi))  # Smooth ease-in-out
    elif easing == "linear":
        pass  # No easing, use t as is
    else:
        raise ValueError(f"Unknown easing function: {easing}")

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