import pygame as pg
import threading
from time import sleep
from resources.py.utils import file_name

fade_time = 200
playing = ''

def fadeout(time):
    pg.mixer_music.fadeout(time)

def play(path):
    # Debug
    print('Now playing: ' + file_name(path))
    # End
    def inner_play():
        global playing
        if playing:
            pg.mixer_music.fadeout(fade_time)
            sleep(fade_time / 1000)
        pg.mixer_music.load(path)
        pg.mixer_music.play(loops=-1)
        playing = path

    t = threading.Thread(target=inner_play)
    t.start()