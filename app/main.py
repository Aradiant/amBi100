# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Imports

import pygame as pg
import threading
import os

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
# Paths

path_userdata = rpath('userdata/save.dat')

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Post-init imports

import engine

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Basic

fps = 50
cur_fps = 50

TEST_ONLY_fps_decrease = 0

width, height = 900, 600

canClick = True

r = 0
g = 0
b = 0
r_lg = 0
g_lg = 0
b_lg = 0

ui_ls = 0.08

main_level_count = 10

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Controls

mdown = False

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Mixer

vol = 0.33

vol_sfx = 0.33

from sfx import *
import music

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Fonts

from fonts import *

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Mode variables

running = True

render = 'Menu'
render_first = {
    'Menu': True,
    'Settings': True,
    'Credits': True,
    'Finish': True,
    'Selector': True
}

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Misc

zoomed = True
zoomed_let_go = True

game_just_finished = False

deaths = 0

music_artists = [
    'Pick Yer Poison',
    'Oxbow',
    'DJ Glejs',
    'JazzCat',
    'snayk',
    'Envy',
    '8 Bit Weapon',
    'SnD',
    'ECLIPSE',
    'Fredulom',
    'Romeo Knight'
]

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Level stats

level_title = ''
level_deaths = 0
level_frames_taken = 0

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Calls

clock = pg.time.Clock()

pg.display.set_caption('amBi100')
screen = pg.display.set_mode((width, height), pg.SCALED)

pg.mixer_music.set_volume(vol)
music.play(rpath('resources/ogg/ambi100.ogg'))

sfx.set_volume(vol_sfx)
sfx_aux.set_volume(vol_sfx)
sfx_obj.set_volume(vol_sfx)
sfx_e.set_volume(vol_sfx)

engine.essential_init()

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Load userdata / Set default

userdatafile = os.path.exists(path_userdata)
if not userdatafile:
    with open(path_userdata, 'w') as f:
        f.write(
            dumps(
                {
                    'deaths': 0,
                    'vol': vol,
                    'vol_sfx': vol_sfx
                }
            )
        )

userdata = ''
with open(path_userdata, 'r') as f:
    userdata = f.read()
userdata = loads(userdata)

# Set variables

deaths = userdata['deaths']
vol = userdata['vol']
vol_sfx = userdata['vol_sfx']

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
    def __init__(self, color, x, y, width, height, font, text='', group=None, func=None, **kwargs):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

        self.hover = False

        self.extra = kwargs

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
                    self.value = ((self.height - self.handle_height - self.handle_y) / (self.height - self.handle_height)) * (self.max_value - self.min_value) + self.min_value

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

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Menu

menu_group = UIGroup()
menu_group.offset = (-width, 0)

def menu_start_click():
    global canClick, render
    canClick = False
    Render('HideMenu')
    sleep(0.5)
    Render('Selector')
    sleep(0.5)
    canClick = True
menu_start = Button((50, 50, 50), 25, 100, 150, 50, font_pixel_32, 'Start', group=menu_group, func=menu_start_click)

def menu_tutorial_click():
    global canClick, render
    canClick = False
    engine.init(rpath('resources/map/tutorial.lua'))
    Render('HideMenu')
    music.fadeout(500)
    sleep(1)
    Render('Game')
menu_tutorial = Button((50, 50, 50), 25, 175, 150, 50, font_pixel_32, 'Tutorial', group=menu_group, func=menu_tutorial_click)

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

def update_deaths():
    menu_deaths.text = f'Deaths: {deaths}'

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

vol_slider = VerticalSlider(85, 100, 150, 0, 1, vol, group=settings_group, func_str='global vol; vol = self.value; pg.mixer_music.set_volume(vol)')
vol_text = Label((255, 255, 255), 25, 260, font_pixel_24, 'Music Volume', group=settings_group)

vol_sfx_slider = VerticalSlider(85, 300, 150, 0, 1, vol_sfx, group=settings_group, func_str='global vol_sfx; vol_sfx = self.value; sfx.set_volume(vol_sfx); sfx_aux.set_volume(vol_sfx); sfx_obj.set_volume(vol_sfx); sfx_e.set_volume(vol_sfx)')
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
credits_5 = Label((255, 255, 255), 25, 260, font_retro_24, 'Music:', group=credits_group)
music_artists_credits = Label((255, 255, 255), 25, 290, font_pixel_32, 'Name', group=credits_group)

def loop_music_artists():
    while True:
        for name in music_artists:
            music_artists_credits.text = name
            sleep(2)
lma_worker = threading.Thread(target=loop_music_artists)
lma_worker.start()

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Level finish

finish_group = UIGroup()
finish_group.offset = (0, -height)

finish_header = Label((255, 255, 255), 25, 25, font_retro_36, 'Level completed!', group=finish_group)
finish_title = Label((255, 255, 255), 25, 75, font_pixel_24, 'Title: Level Title', group=finish_group)
finish_deaths = Label((255, 255, 255), 25, 105, font_pixel_24, 'Deaths: 0', group=finish_group)
finish_time = Label((255, 255, 255), 25, 135, font_pixel_24, 'Time taken: 00:00.000', group=finish_group)

def finish_back_click():
    global canClick, render
    canClick = False
    Render('Menu')
    music.play(rpath('resources/ogg/ambi100.ogg'))
    sleep(1)
    canClick = True
finish_back = Button((50, 50, 50), 25, height - 75, 150, 50, font_pixel_32, 'Back', group=finish_group, func=finish_back_click)

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Level selector

selector_group = UIGroup()
selector_group.offset = (0, -height)

selector_header = Label((255, 255, 255), 25, 25, font_retro_36, 'Levels', group=selector_group)

def selector_back_click():
    global canClick, render
    canClick = False
    Render('Menu')
    sleep(1)
    canClick = True
selector_back = Button((50, 50, 50), 25, height - 75, 150, 50, font_pixel_32, 'Back', group=selector_group, func=selector_back_click)

_grid_width = 5
lbs = []
for _i in range(0, main_level_count):
    i = _i + 1
    base_path = rpath('resources/map')
    base_path += '/' + str(i) + '.lua'
    if os.path.exists(base_path):
        def new_button_func(a=base_path):
            # Level load
            global canClick, render
            canClick = False
            engine.init(a)
            Render('HideMenu')
            music.fadeout(500)
            sleep(1)
            Render('Game')
        lbs.append(
            Button((100, 100, 100),
                   110 + width // 2 + (width // _grid_width - 10) * (i - math.ceil(_grid_width / 2)),
                   -100 + height // 2, 75, 75, font_retro_24,
                   str(i),
                   group=selector_group,
                   func=new_button_func)
        )

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Stuff that hasn't been caught up

update_deaths()

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# PG loop

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            if render == 'Game':
                music.play(rpath('resources/ogg/ambi100.ogg'))
                render = 'Menu'
                canClick = True
                sfx.play(sfx_uiback)

                update_deaths()
            else:
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
                case 'Finish':
                    finish_group.click()
                case 'Selector':
                    selector_group.click()

        if event.type == pg.MOUSEBUTTONUP:
            mdown = False

    screen.fill((r, g, b))

    # Background lerp logic
    if r != r_lg:
        r = lerp(r, r_lg, 0.13, easing='ease_out')
    if g != g_lg:
        g = lerp(g, g_lg, 0.13, easing='ease_out')
    if b != b_lg:
        b = lerp(b, b_lg, 0.13, easing='ease_out')
    # End

    match render:
        case 'Menu':
            if render_first[render]:
                menu_group.offset = (-width, 0)
            menu_group.offset = (lerp(menu_group.offset[0], 0, ui_ls), 0)

            menu_group.updateHover()

            settings_group.offset = (lerp(settings_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)
            credits_group.offset = (lerp(credits_group.offset[0], -width, ui_ls * 3, easing='ease_in'), 0)
            finish_group.offset = (0, lerp(finish_group.offset[1], -height, ui_ls * 4.5, easing='ease_in'))
            selector_group.offset = (0, lerp(selector_group.offset[1], -height, ui_ls * 4.5, easing='ease_in'))
        
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

        case 'HideMenu':
            menu_group.offset = (lerp(menu_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)

        case 'Finish':
            if game_just_finished:
                render_first[render] = True
                game_just_finished = False
                update_deaths()

                finish_title.text = 'Title: ' + level_title
                finish_deaths.text = 'Deaths: ' + str(level_deaths)
                finish_time.text = 'Time taken: ' + frames_to_time(level_frames_taken)

                music.play(rpath('resources/ogg/ambi100bass.ogg'))

            if render_first[render]:
                finish_group.offset = (0, -height)
            
            finish_group.updateHover()

            finish_group.offset = (0, lerp(finish_group.offset[1], 0, ui_ls * 0.38, easing='ease_out'))

            menu_group.offset = (lerp(menu_group.offset[0], -width, ui_ls * 2, easing='ease_in'), 0)

            selector_group.offset = (0, lerp(selector_group.offset[1], -height, ui_ls * 100, easing='ease_in'))
        
        case 'Selector':
            if render_first[render]:
                selector_group.offset = (0, -height)
            
            selector_group.updateHover()

            selector_group.offset = (0, lerp(selector_group.offset[1], 0, ui_ls))

            menu_group.offset = (lerp(menu_group.offset[0], -width, 1, easing='ease_in'), 0)

    if render != 'Game':
        menu_group.draw(screen)
        settings_group.draw(screen)
        credits_group.draw(screen)
        finish_group.draw(screen)
        selector_group.draw(screen)
    else:
        engine.update()
        engine.render(screen)

        if zoomed:
            screen.blit(pg.transform.scale_by(screen, 2), (-width // 2, -height // 2))

        z = pg.key.get_pressed()[pg.K_z]
        if not z:
            zoomed_let_go = True
        if z and zoomed_let_go:
            zoomed = not zoomed
            zoomed_let_go = False

    if render_first[render]:
        render_first[render] = False

    clock.tick(fps - TEST_ONLY_fps_decrease)
    cur_fps = clock.get_fps()

    # FPS counter
    screen.blit(font_pixel_16_bold.render('FPS: ' + str(int(cur_fps)), False, (255, 255, 255), (0, 0, 0)), (width - 44, height - 15))

    pg.display.flip()

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Save userdata
    
with open(path_userdata, 'w') as f:
    f.write(
        dumps(
            {
                'deaths': deaths,
                'vol': vol,
                'vol_sfx': vol_sfx
            }
        )
    )
    
# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Quit
        
pg.quit()