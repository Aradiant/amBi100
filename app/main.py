# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Imports

import pygame as pg
import math
from json import dumps, loads

from resources.py.utils import *

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Presets, initialization

pg.init()

clock, fps = pg.time.Clock(), 50

pg.display.set_caption('amBi100')

width, height = 900, 600
screen = pg.display.set_mode((width, height), pg.SCALED)

r = 0
g = 0
b = 0

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Fonts

font_retro_50 = pg.font.Font(rpath('resources/ttf/retrogaming.ttf'), 50)
font_pixel_32 = pg.font.Font(rpath('resources/ttf/pixeloperator.ttf'), 32)

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Mode variables

running = True
render = 'Menu'

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# UI classes

class Button:
    def __init__(self, color, x, y, width, height, font, text='', group=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

        self.hover = False

        if group:
            group.add(self)

    def draw(self, win):
        pg.draw.rect(win, [self.color, brighten(self.color)][self.hover], (self.x - 2, self.y - 2, self.width + 4, self.height + 4), [4, 0][self.hover])
        
        if self.text != '':
            text = self.font.render(self.text, 1, [(255, 255, 255), (0, 0, 0)][self.hover])
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isHover(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.hover = True
                return
            
        self.hover = False

class ButtonGroup:
    def __init__(self):
        self.d = {}
    
    def add(self, btn):
        if not self.d.get(id(btn), False):
            self.d[id(btn)] = btn
        else:
            print(f'ButtonGroup: Button "{btn.text}" already added')

    def updateHover(self):
        mpos = pg.mouse.get_pos()
        for i in self.d.values():
            i.isHover(mpos)

    def draw(self, win):
        for i in self.d.values():
            i.draw(win)


# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Sprite classes
    
# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Create instances

menu_group = ButtonGroup()

menu_start = Button((50, 50, 50), 25, 100, 150, 50, font_pixel_32, 'Start', group=menu_group)
menu_tutorial = Button((50, 50, 50), 25, 175, 150, 50, font_pixel_32, 'Tutorial', group=menu_group)
menu_settings = Button((50, 50, 50), 25, 250, 150, 50, font_pixel_32, 'Settings', group=menu_group)
menu_quit = Button((100, 0, 0), 25, 325, 150, 50, font_pixel_32, 'Quit', group=menu_group)

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# PG loop

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((r, g, b))

    match render:
        case 'Menu':
            menu_header = font_retro_50.render('amBi100', True, 'white')

            screen.blit(menu_header, (25, 25))

            menu_group.updateHover()
            menu_group.draw(screen)
    

    pg.display.flip()
    clock.tick(fps)
        
pg.quit()