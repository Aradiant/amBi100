import pygame as pg
from resources.py.utils import *

sfx = pg.mixer.Channel(1)
sfx_aux = pg.mixer.Channel(2)
sfx_obj = pg.mixer.Channel(3)

sfx_e = pg.mixer.Channel(4)
sfx_e_pos = pg.mixer.Sound(rpath('resources/ogg/_emotion_positive.ogg'))
sfx_e_neg = pg.mixer.Sound(rpath('resources/ogg/_emotion_negative.ogg'))
sfx_e_s_pos = pg.mixer.Sound(rpath('resources/ogg/_emotion_slightly_positive.ogg'))
sfx_e_s_neg = pg.mixer.Sound(rpath('resources/ogg/_emotion_slightly_negative.ogg'))
sfx_e_m_neg = pg.mixer.Sound(rpath('resources/ogg/_emotion_mildly_negative.ogg'))

sfx_exit = pg.mixer.Sound(rpath('resources/ogg/_exit.ogg'))
sfx_click = pg.mixer.Sound(rpath('resources/ogg/_click.ogg'))
sfx_select = pg.mixer.Sound(rpath('resources/ogg/_select.ogg'))
sfx_unselect = pg.mixer.Sound(rpath('resources/ogg/_unselect.ogg'))
sfx_forbid = pg.mixer.Sound(rpath('resources/ogg/_forbid.ogg'))
sfx_jump = pg.mixer.Sound(rpath('resources/ogg/_jump.ogg'))
sfx_djump = pg.mixer.Sound(rpath('resources/ogg/_jumpsecond.ogg'))
sfx_checkpoint = pg.mixer.Sound(rpath('resources/ogg/_checkpoint.ogg'))
sfx_reveal = pg.mixer.Sound(rpath('resources/ogg/_reveal.ogg'))
sfx_deadlyreveal = pg.mixer.Sound(rpath('resources/ogg/_deadlyreveal.ogg'))
sfx_die = pg.mixer.Sound(rpath('resources/ogg/_die.ogg'))
sfx_uiback = pg.mixer.Sound(rpath('resources/ogg/_uiback.ogg'))