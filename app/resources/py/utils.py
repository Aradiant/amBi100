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
    return fspath(Path(__file__).parent.parent.parent / obj).replace('\\', '/')

def brighten(color, m=255):
    '''Make RGB color components m, if above 0'''
    return ([0, m][bool(color[0])], [0, m][bool(color[1])], [0, m][bool(color[2])])

def now():
    '''Get amount of seconds since the epoch'''
    return time()

def frames_to_time(frames, fps=50):
    '''Return formatted time from given frames'''
    h = frames // (3600*fps)
    m = frames // (60*fps) % 60
    s = frames // fps % 60
    ms = int(frames % fps / fps * 1000)

    h, m, s, ms = str(h).rjust(2, '0'), str(m).rjust(2, '0'), str(s).rjust(2, '0'), str(ms).rjust(3, '0')

    return f'{["", h + ":"][bool(int(h))]}' + f'{m}:{s}.{ms}'

def file_name(path):
    '''Extract file name from path'''
    return path.split('/')[::-1][0]

def extract_map_title(path):
    '''Extract the map\'s title, without loading it'''
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for d in data:
            index = d.find('title')
            if index != -1:
                sd = d.split('=')
                use_next = False
                for e in sd:
                    if use_next:
                        return e.strip().replace(e.strip()[0], '')
                    if 'title' in e:
                        use_next = True