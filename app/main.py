# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Imports

import pygame as pg
import threading
import math
from time import sleep
from json import dumps, loads

from resources.py.utils import *

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Global functions

def Render(v):
    global render
    render = v
    render_first[v] = True

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Preset and init work

pg.init()
pg.mixer.init()

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Basic

fps = 50
width, height = 900, 600

canClick = True

r = 0
g = 0
b = 0

ui_ls = 0.08

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Controls

mdown = False

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Mixer

vol = 0.33

vol_sfx = 0.33

sfx = pg.mixer.Channel(1)

sfx_exit = pg.mixer.Sound(rpath('resources/ogg/_exit.ogg'))
sfx_click = pg.mixer.Sound(rpath('resources/ogg/_click.ogg'))
sfx_select = pg.mixer.Sound(rpath('resources/ogg/_select.ogg'))
sfx_unselect = pg.mixer.Sound(rpath('resources/ogg/_unselect.ogg'))
sfx_forbid = pg.mixer.Sound(rpath('resources/ogg/_forbid.ogg'))

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Fonts

font_retro_50 = pg.font.Font(rpath('resources/ttf/retrogaming.ttf'), 50)
font_retro_24 = pg.font.Font(rpath('resources/ttf/retrogaming.ttf'), 24)
font_pixel_32 = pg.font.Font(rpath('resources/ttf/pixeloperator.ttf'), 32)
font_pixel_32_italic = pg.font.Font(rpath('resources/ttf/pixeloperator.ttf'), 32); font_pixel_32_italic.italic = True
font_pixel_24 = pg.font.Font(rpath('resources/ttf/pixeloperator.ttf'), 24)

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Mode variables

running = True

render = 'Menu'
render_first = {
    'Menu': True,
    'Settings': True,
    'Credits': True
}

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Misc

deaths = 0

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Calls

clock = pg.time.Clock()

pg.display.set_caption('amBi100')
screen = pg.display.set_mode((width, height), pg.SCALED)

pg.mixer_music.set_volume(vol)
pg.mixer_music.load(rpath('resources/ogg/ambi100.ogg'))
pg.mixer_music.play(loops=-1)

sfx.set_volume(vol_sfx)

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# UI classes

class Label:
    def __init__(self, color, x, y, font, text='', group=None):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.font = font

        if group:
            group.add(self)

    def draw(self, win, offset=(0, 0)):
        if self.text != '':
            text = self.font.render(self.text, 1, self.color)
            win.blit(text, (self.x + offset[0], self.y + offset[1]))

class Button:
    def __init__(self, color, x, y, width, height, font, text='', group=None, func=None):
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
        if not func:
            print('Button: MUST provide function for button upon creation')
        else:
            self.func = func

    def draw(self, win, offset=(0, 0)):
        x, y = self.x + offset[0], self.y + offset[1]
        pg.draw.rect(win, [self.color, brighten(self.color)][self.hover], (x - 2, y - 2, self.width + 4, self.height + 4), [4, 0][self.hover])
        if self.hover:
            pg.draw.rect(win, brighten(self.color, m=225), (x - 2, y - 2, self.width + 4, self.height + 4), 4)
        
        if self.text != '':
            text = self.font.render(self.text, 1, [(255, 255, 255), (0, 0, 0)][self.hover])
            win.blit(text, (x + (self.width / 2 - text.get_width() / 2), y + (self.height / 2 - text.get_height() / 2)))

    def isHover(self, pos, offset=(0, 0)):
        x, y = self.x + offset[0], self.y + offset[1]
        if pos[0] > x and pos[0] < x + self.width:
            if pos[1] > y and pos[1] < y + self.height:
                self.hover = True
                return
            
        self.hover = False

    def click(self):
        if canClick:
            sfx.play(sfx_click)
            funcThread = threading.Thread(target=self.func)
            funcThread.start()

class VerticalSlider:
    def __init__(self, x, y, height, min_value, max_value, initial_value, group=None, func_str=None):
        self.x = x
        self.y = y
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        self.track_width = 5
        self.handle_width = 50
        self.handle_height = 10

        self.track_color = (50, 50, 50)
        self.handle_color = (255, 255, 255)

        self.handle_y = self.height - (self.height * (self.value / self.max_value))

        if group:
            group.add(self)
        if not func_str:
            print('VerticalSlider: MUST provide function code for slider upon creation')
        else:
            self.func_str = func_str

    def draw(self, win, offset=(0, 0)):
        x, y = self.x + offset[0], self.y + offset[1]
        pg.draw.rect(
            win,
            self.track_color,
            (x - self.track_width // 2, y, self.track_width, self.height),
        )

        pg.draw.rect(
            win,
            self.handle_color,
            (
                x - self.handle_width // 2,
                y + self.handle_y,
                self.handle_width,
                self.handle_height,
            ),
        )
    
    def update(self, offset=(0, 0)):
        if not canClick:
            return

        x, y = self.x + offset[0], self.y + offset[1]
        mpos = pg.mouse.get_pos()

        handle_rect = pg.Rect(
                x - self.handle_width // 2,
                y + self.handle_y,
                self.handle_width,
                self.handle_height,
            )
        if handle_rect.collidepoint(mpos):
            def inner_update():
                self.track_color = (100, 100, 100)
                sfx.play(sfx_select)
                while mdown:
                    mpos = pg.mouse.get_pos()
                    self.handle_y = clamp(mpos[1] - y, 0, self.height - self.handle_height)
                    self.value = ((self.height - self.handle_y) / (self.height - self.handle_height)) * (self.max_value - self.min_value) + self.min_value

                    exec(self.func_str)
                    sleep(0.005)
                self.track_color = (50, 50, 50)
                sfx.play(sfx_unselect)
            
            iu = threading.Thread(target=inner_update)
            iu.start()

class UIGroup:
    def __init__(self):
        self.d = {}
        self.offset = (0, 0)
    
    def add(self, btn):
        if not self.d.get(id(btn), False):
            self.d[id(btn)] = btn
        else:
            print(f'UIGroup: Object "{btn.text}" already added')

    def updateHover(self):
        mpos = pg.mouse.get_pos()
        for i in self.d.values():
            if i.__class__.__name__ == 'Button':
                i.isHover(mpos, self.offset)
    
    def click(self):
        for i in self.d.values():
            match i.__class__.__name__:
                case 'Button':
                    if i.hover:
                        i.click()
                case 'VerticalSlider':
                    i.update(self.offset)

    def draw(self, win):
        for i in self.d.values():
            i.draw(win, offset=self.offset)

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Sprite classes

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Create instances

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Menu

menu_group = UIGroup()
menu_group.offset = (-width, 0)

menu_start = Button((50, 50, 50), 25, 100, 150, 50, font_pixel_32, 'Start', group=menu_group)
menu_tutorial = Button((50, 50, 50), 25, 175, 150, 50, font_pixel_32, 'Tutorial', group=menu_group)

def menu_settings_click():
    global canClick, render
    canClick = False
    Render('Settings')
    sleep(1)
    canClick = True
menu_settings = Button((50, 50, 50), 25, 250, 150, 50, font_pixel_32, 'Settings', group=menu_group, func=menu_settings_click)

def menu_credits_click():
    global canClick, render
    canClick = False
    Render('Credits')
    sleep(1)
    canClick = True
menu_credits = Button((50, 50, 50), 25, 325, 150, 50, font_pixel_32, 'Credits', group=menu_group, func=menu_credits_click)

def menu_quit_click():
    global running, canClick, fps
    canClick = False
    fps = 1 / 2.75

    pg.mixer_music.fadeout(333)
    sfx.play(sfx_exit)

    sleep(2.5)
    running = False
menu_quit = Button((100, 0, 0), 25, 400, 150, 50, font_pixel_32, 'Quit', group=menu_group, func=menu_quit_click)

menu_header = Label((255, 255, 255), 25, 25, font_retro_50, 'amBi100', group=menu_group)
menu_deaths = Label((255, 255, 255), 12, height - 30, font_pixel_24, 'Deaths: 0', group=menu_group)

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Settings

settings_group = UIGroup()
settings_group.offset = (-width, 0)

def settings_back_click():
    global canClick, render
    canClick = False
    Render('Menu')
    sleep(1)
    canClick = True
settings_back = Button((50, 50, 50), 25, height - 75, 150, 50, font_pixel_32, 'Back', group=settings_group, func=settings_back_click)

vol_slider = VerticalSlider(85, 100, 150, 0, 1, vol, group=settings_group, func_str='vol = self.value; pg.mixer_music.set_volume(vol)')
vol_text = Label((255, 255, 255), 25, 260, font_pixel_24, 'Music Volume', group=settings_group)

vol_sfx_slider = VerticalSlider(85, 300, 150, 0, 1, vol_sfx, group=settings_group, func_str='vol_sfx = self.value; sfx.set_volume(vol_sfx)')
vol_sfx_text = Label((255, 255, 255), 35, 460, font_pixel_24, 'SFX Volume', group=settings_group)

settings_header = Label((255, 255, 255), 25, 25, font_retro_50, 'Settings', group=settings_group)

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Credits

credits_group = UIGroup()
credits_group.offset = (-width, 0)

def credits_back_click():
    global canClick, render
    canClick = False
    Render('Menu')
    sleep(1)
    canClick = True
credits_back = Button((50, 50, 50), 25, height - 75, 150, 50, font_pixel_32, 'Back', group=credits_group, func=credits_back_click)

credits_header = Label((255, 255, 255), 25, 25, font_retro_50, 'Credits', group=credits_group)
credits_1 = Label((255, 255, 255), 25, 100, font_retro_24, 'Programming, Graphics, SFX, Levels, Story:', group=credits_group)
credits_2 = Label((255, 255, 255), 25, 130, font_pixel_32, 'Aradiant', group=credits_group)
credits_3 = Label((255, 255, 255), 25, 180, font_pixel_32_italic, 'Written on PyGame', group=credits_group)
credits_4 = Label((255, 255, 255), 25, 210, font_pixel_32_italic, 'and compiled with PyInstaller', group=credits_group)

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# PG loop

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sfx.play(sfx_forbid)

        if event.type == pg.MOUSEBUTTONDOWN:
            mdown = True
            match render:
                case 'Menu':
                    menu_group.click()
                case 'Settings':
                    settings_group.click()
                case 'Credits':
                    credits_group.click()

        if event.type == pg.MOUSEBUTTONUP:
            mdown = False


    screen.fill((r, g, b))

    match render:
        case 'Menu':
            if render_first[render]:
                menu_group.offset = (-width, 0)
            menu_group.offset = (lerp(menu_group.offset[0], 0, ui_ls), 0)

            menu_group.updateHover()

            settings_group.offset = (lerp(settings_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)
            credits_group.offset = (lerp(credits_group.offset[0], -width, ui_ls * 3, easing='ease_in'), 0)
        
        case 'Settings':
            if render_first[render]:
                settings_group.offset = (-width, 0)
            settings_group.offset = (lerp(settings_group.offset[0], 0, ui_ls), 0)

            settings_group.updateHover()

            menu_group.offset = (lerp(menu_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)

        case 'Credits':
            if render_first[render]:
                credits_group.offset = (-width, 0)
            credits_group.offset = (lerp(credits_group.offset[0], 0, ui_ls), 0)

            credits_group.updateHover()

            menu_group.offset = (lerp(menu_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)
            
    if render != 'Game':
        menu_group.draw(screen)
        settings_group.draw(screen)
        credits_group.draw(screen)

    if render_first[render]:
        render_first[render] = False

    pg.display.flip()
    clock.tick(fps)
        
pg.quit()