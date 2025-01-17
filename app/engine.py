# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Imports

import pygame as pg
import math
import threading
from json import loads
from time import sleep

import inspect

from resources.py.utils import *

from sfx import *
import music
from fonts import *

from lupa.lua54 import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=False)
lua.execute(f'package.path = package.path .. ";{rpath("resources/lua/?.lua")}"')

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Initialization data

width, height = 900, 600
plat_w, plat_h = 30, 30

map_path = ''

nothing_char = ''
plr_char = ''
data = {}
map_data = ''
map_track = ''
map_title = ''
level_end_char = ''
level_end_state = ''

level_finished = False

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Player stats

plr = None

plr_mv_walk = 2
plr_mv = 4
plr_mv_loss = 1.5
plr_max_yvel = 10
plr_sx = 0
plr_sy = 0

plr_w, plr_h = 21, 40

gravity = 0.35
jump = 8

can_double_jump = True
jump_let_go = True
restart_let_go = True

last_checkpoint = None

dead = False

frames_taken = 0

# - — - — - — - — - — - — - — - — - - — - — - — - — - — - — - —
# Misc

first_update = True

st = None
st_atlas = None

objects = pg.sprite.Group()
entities = pg.sprite.Group()
misc = []

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Low-level functions

def set_main_variable(name, v):
    caller_frame = inspect.currentframe()
    while caller_frame.f_globals['__name__'] != '__main__':
        caller_frame = caller_frame.f_back
    caller_frame.f_globals[name] = v

    del caller_frame

def get_main_variable(name):
    caller_frame = inspect.currentframe()
    while caller_frame.f_globals['__name__'] != '__main__':
        caller_frame = caller_frame.f_back
    temp = caller_frame.f_globals[name]

    del caller_frame

    return temp

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Classes

class AnimatedSprite(pg.sprite.Sprite):
    def __init__(self, group, dict):
        '''
        Accepts spritesheet data as a dictionary with lists.
        Example: {'walking':[spritesheet, rows, columns, time (in frames)]

        Make sure to set self.state and call self.animate() after init.

        Note that this class is used a shell for other classes, therefore it does not have coordinate initialization.
        Rect initialization should also be done inside the class that inherits this one.
        '''
        self.frame_counter = 0
        self.frame_wait = 0

        self.last_state = None
        self.state = None
        super().__init__(group)
        for k, v in dict.items():
            sheet = load_image(rpath(v[0]))
            rows, columns = v[1], v[2]
            w, h = sheet.get_width() // columns, sheet.get_height() // rows

            k_frames = k + '_frames'
            k_time = k + '_time'

            frames = []
            for xi in range(columns):
                for yi in range(rows):
                    frames.append(sheet.subsurface(pg.Rect(w * xi, h * yi, w, h)))
            
            setattr(self, k_frames, frames)
            setattr(self, k_time, v[3])
    
    def change_state(self, s):
        self.state = s
        if self.state != self.last_state:
            self.frame_counter = 0
            self.frame_wait = 0
        self.last_state = s

    def animate(self):
        frames = getattr(self, self.state + '_frames')
        self.image = frames[self.frame_counter]
        time_required = getattr(self, self.state + '_time')
        if self.frame_wait < time_required:
            self.frame_wait += 1
            return
        self.frame_wait = 0
        self.frame_counter = (self.frame_counter + 1) % len(frames)

class Player(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(entities, {
            'idle': ['resources/png/char_idle.png', 1, 2, 50],
            'win': ['resources/png/char_win.png', 1, 1, 0],
            'move_slow': ['resources/png/char_move.png', 1, 4, 10],
            'move': ['resources/png/char_move_fast.png', 1, 4, 6],
            'fall': ['resources/png/char_fall.png', 1, 2, 11],
            'fall_side': ['resources/png/char_fall_side.png', 1, 2, 11],
            'jump': ['resources/png/char_jump.png', 1, 2, 11],
            'jump_side': ['resources/png/char_jump_side.png', 1, 2, 11]
            })
        self.state = 'idle'
        self.animate()

        self.flipped = False

        self.xvel = 0
        self.yvel = 0

        self.custom_mask = pg.mask.from_surface(load_image(rpath('resources/png/char_mask.png')))
        self.custom_mask_precise = pg.mask.from_surface(load_image(rpath('resources/png/char_mask_precise.png')))
        self.mask_w, self.mask_h = get_rect_mask_dimensions(self.custom_mask, only_size=True)
        self.mask_w, self.mask_h = (plr_w - self.mask_w) // 2, plr_h - self.mask_h

        self.rect = pg.Rect(x, y, plr_w, plr_h)

        self.ground_tick = 0
        self.max_ground_tick = 4
        self.jump_tick = 0
        self.max_jump_tick = 50

        self.air_last = 0
    
    def change_state(self, s):
        if s in 'win':
            self.state = s
            self.air_last = 0

        if self.air_last and s != 'air':
            self.air_last -= 1
            return
        self.state = s
        
        if self.state != self.last_state:
            self.frame_counter = 0
            self.frame_wait = 0
        self.last_state = s

        if s == 'air':
            self.air_last = 2

    def animate(self):
        frames = ''
        time_required = 0

        if self.state != 'air':
            frames = getattr(self, self.state + '_frames')
            time_required = getattr(self, self.state + '_time')
        else:
            # If in air
            air_state_name = ['fall', 'jump'][self.yvel <= 0]
            # if self.xvel != 0:
                # air_state_name += '_side'
            frames = getattr(self, air_state_name + '_frames')
            time_required = getattr(self, air_state_name + '_time')
        self.image = frames[self.frame_counter]
        if self.frame_wait < time_required:
            self.frame_wait += 1
            return
        self.frame_wait = 0
        self.frame_counter = (self.frame_counter + 1) % len(frames)
    
    def check_collision(self, mode):
        global can_double_jump, plr_sx, plr_sy, last_checkpoint, level_finished

        # Check platforms
        c_sprites = pg.sprite.spritecollide(sprite=self, group=objects, dokill=0)

        for c_sprite in c_sprites:
            c_sprite_mask = pg.mask.from_surface(c_sprite.image)

            # Check with mask accuracy for all
            intrsct = c_sprite_mask.overlap(self.custom_mask, 
                                            offset=(self.rect.x - c_sprite.rect.x , self.rect.y - c_sprite.rect.y))
            if not intrsct:
                continue

            deadly = getattr(c_sprite, 'kills', False)
            has_hit_action = getattr(c_sprite, 'hit_action', False)
            
            # Check if has custom collision logic
            def call_hit_action():
                if has_hit_action:
                    c_sprite.hit_action = c_sprite.hit_action.strip()
                    def exec_hit_action():
                        exec(c_sprite.hit_action)
                    exec_t = threading.Thread(target=exec_hit_action)
                    exec_t.start()
            
            if not deadly:
                call_hit_action()

            # Check if colliding sprite is deadly, then check collision by precise mask
            if deadly:
                if c_sprite_mask.overlap(self.custom_mask_precise, 
                                         offset=(self.rect.x - c_sprite.rect.x , self.rect.y - c_sprite.rect.y)):
                    call_hit_action()
                    die()
                continue

            # We assume that every normal platform has rectangular graphics
            # Calculate height and width of c_sprite mask filled bits
            cs_x, cs_y, cs_w, cs_h = get_rect_mask_dimensions(c_sprite_mask)
            # Calculate end

            match mode:
                case 0:
                    if self.xvel > 0:
                        self.rect.right = c_sprite.rect.left + cs_x + self.mask_w
                    elif self.xvel < 0:
                        self.rect.left = c_sprite.rect.left + cs_w + cs_x - self.mask_w
                case 1:
                    if self.yvel > 0:
                        # Landing
                        self.rect.bottom = c_sprite.rect.top + cs_y
                        self.ground_tick = self.max_ground_tick
                        self.yvel = 0

                        can_double_jump = True
                    elif self.yvel < 0:
                        # Ceiling hit
                        self.rect.top = c_sprite.rect.top + cs_h + cs_y - self.mask_h
                        self.yvel = 0
                        self.jump_tick = self.max_jump_tick
        
        # Check entities
        e_sprites = pg.sprite.spritecollide(sprite=self, group=entities, dokill=0)

        for e_sprite in e_sprites:
            if e_sprite.__class__.__name__ == 'Checkpoint' and last_checkpoint != e_sprite.rect:
                last_checkpoint = e_sprite.rect
                plr_sx, plr_sy = e_sprite.rect.x + 4, e_sprite.rect.y - 10
                sfx_e.play(sfx_e_s_pos)

                def p():
                    sleep(1/5)
                    sfx_aux.play(sfx_checkpoint)
                pt = threading.Thread(target=p)
                pt.start()

            elif e_sprite.__class__.__name__ == 'LevelEnd':
                self.change_state('win')
                level_finished = True

    def update(self, keys):
        global jump_let_go, restart_let_go, can_double_jump, dead

        self.image.set_alpha(255 * (not dead))

        # Restart check
        if keys[pg.K_r] and restart_let_go:
            restart_let_go = False
            restart()
        if not keys[pg.K_r]:
            restart_let_go = True

        # Do nothing if dead
        if dead:
            return
        
        # Check the other keys
        if keys[pg.K_RIGHT] and keys[pg.K_LEFT]:
            self.change_state('idle')
            self.xvel = math.copysign(max(0, abs(self.xvel) - plr_mv_loss), self.xvel)
        else:
            if not keys[pg.K_s]:
                # player let go of jump
                jump_let_go = True

            if keys[pg.K_s]:
                
                # Jump height is bound to how long the jump key is held
                def jump_held():
                    self.jump_tick = 0
                    while not jump_let_go and self.jump_tick < self.max_jump_tick:
                        self.yvel = -jump / 1.75
                        self.jump_tick += 1
                        sleep(1 / 333)
                
                # Perform a normal jump
                if self.ground_tick and jump_let_go:
                    self.ground_tick = 0
                    # self.yvel = -jump
                    sfx.play(sfx_jump)

                    jump_let_go = False

                    jt = threading.Thread(target=jump_held)
                    jt.start()

                # Perform a double jump
                if not self.ground_tick and jump_let_go and can_double_jump:
                    # self.yvel = -jump
                    sfx.play(sfx_djump)

                    can_double_jump = False
                    jump_let_go = False

                    jt = threading.Thread(target=jump_held)
                    jt.start()

                jump_let_go = False

            vel = [plr_mv, plr_mv_walk][keys[pg.K_a]]
            if keys[pg.K_LEFT]:
                self.xvel = -vel
                self.flipped = True

            if keys[pg.K_RIGHT]:
                self.xvel = vel
                self.flipped = False
            
            if not (keys[pg.K_RIGHT] or keys[pg.K_LEFT]):
                self.change_state('idle')
                self.xvel = math.copysign(max(0, abs(self.xvel) - plr_mv_loss), self.xvel)
            else:
                if keys[pg.K_a]:
                    self.change_state('move_slow')
                else:
                    self.change_state('move')
        # End
        
        if self.ground_tick < self.max_ground_tick:
            self.yvel = min(self.yvel + gravity, plr_max_yvel)
        self.ground_tick = max(self.ground_tick - 1, 0)

        # Air animation if ground tick is 0
        if self.ground_tick == 0:
            self.change_state('air')

        self.rect.x += self.xvel
        self.check_collision(0)
        self.rect.y += self.yvel
        self.check_collision(1)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, surface, **kwargs):
        super().__init__(objects)
        self.image = surface
        self.rect = pg.Rect(x, y, plat_w, plat_h)

        for k, v in kwargs.items():
            setattr(self, k, v)
        
        # Custom action
        if getattr(self, 'action', False):
            self.action = self.action.strip()
            def exec_action():
                exec(self.action)
            exec_t = threading.Thread(target=exec_action)
            exec_t.start()

class Checkpoint(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(entities, {
            'default': ['resources/png/checkpoint.png', 4, 1, 8]
        })
        self.state = 'default'
        self.animate()
        self.rect = pg.Rect(x, y, plat_w, plat_h)

class LevelEnd(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(entities, {
            'default': ['resources/png/levelend.png', 5, 1, 5]
        })
        self.state = 'default'
        self.animate()

        self.rect = pg.Rect(x, y, plat_w, plat_h)

class Text:
    def __init__(self, x, y, text, font, color, ox=0, oy=0):
        global misc
        self.x, self.y = x, y
        self.text = text
        self.font = font
        self.color = color

        self.ox, self.oy = ox, oy

        misc.append(self)

    def draw(self, win, offset=(0, 0)):
        if self.text != '':
            text = self.font.render(self.text, 1, self.color)
            win.blit(text, (self.ox + self.x + plat_w // 2 - text.get_width() / 2 + offset[0], self.oy + self.y + plat_h // 2 - text.get_height() / 2 + offset[1]))

# -—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-—-
# Functions
            
def die():
    global dead
    dead = True
    sfx_e.play(sfx_e_neg)

    def p():
        sleep(1/6)
        sfx_aux.play(sfx_die)
    pt = threading.Thread(target=p)
    pt.start()

    set_main_variable('r', 25)

    # Counter
    set_main_variable('deaths', get_main_variable('deaths') + 1)
    set_main_variable('level_deaths', get_main_variable('level_deaths') + 1)
            
def restart():
    global plr, map_path, dead

    if not dead:
        sfx_e.play(sfx_e_s_neg)
    else:
        sfx_e.play(sfx_e_m_neg)

    dead = False
    load_map(map_path, soft=True)

    plr.rect.x = plr_sx
    plr.rect.y = plr_sy
    plr.xvel = 0
    plr.yvel = 0

def get_rect_mask_dimensions(mask, only_size=False):
    mask_w, mask_h = 0, 0
    mask_x, mask_y = -1, -1
    for _x in range(0, mask.get_size()[0]):
        for _y in range(0, mask.get_size()[1]):
            if mask.get_at((_x, _y)):
                if mask_x < 0 and mask_y < 0:
                    mask_x, mask_y = _x, _y
                    break
        if mask_x >= 0 and mask_y >= 0:
            break
    for _x in range(mask_x, mask.get_size()[0]):
        if mask.get_at((_x, mask_y)):
            mask_w += 1
        else:
            break
    for _y in range(mask_y, mask.get_size()[1]):
        if mask.get_at((mask_x, _y)):
            mask_h += 1
        else:
            break
    if only_size:
        return mask_w, mask_h
    return mask_x, mask_y, mask_w, mask_h
        
def load_image(path, alpha=True):
    image = pg.image.load(path)
    if alpha:
        image.convert_alpha()
    return image
        
def load_map(path, soft=False):
    global plr_char, data, map_data, nothing_char, plr_sx, plr_sy, map_track, plr, level_end_char, level_end_state, map_title

    if soft:
        entities.empty()
        objects.empty()

    base_lua = '''
    local plr = ''
    local data = {}
    local map = ''
    local nothing = ''
    local track = ''
    local level_end = ''
    local title = ''
    '''

    with open(path, 'r') as f:
        base_lua += f.read()
    base_lua += '''
    return plr, data, map, nothing, track, level_end, title
    '''

    plr_char, data, map_data, nothing_char, map_track, level_end, map_title = lua.execute(base_lua)
    level_end = eval(level_end)
    level_end_char, level_end_state = level_end[0], level_end[1]

    data = dict(data)
    for k, i in data.items():
        data[k] = dict(i)
    
    map_data = map_data.strip()

    plr_i = map_data.find(plr_char)
    temp = map_data[:plr_i]
    row = temp.count('\n')
    col = map_data.split('\n')[row].find(plr_char)
    if not soft:
        plr_sx = col * plat_w + 4
        plr_sy = row * plat_h + 20

    # Load map tiles into objects
    level = map_data.split('\n')
    x, y = 0, 0
    for row in level:
        for col in row:
            if col == level_end_char:
                LevelEnd(x, y)
                x += plat_w
                continue

            if col in nothing_char + plr_char:
                x += plat_w
                continue

            tile_data = dict(data[col])
            tile_class = tile_data['class']
            match tile_class:
                case 'Platform':
                    kwargs_string = ''
                    for k, v in tile_data.items():
                        if k in ['class', 'tile']:
                            continue
                        kwargs_string += str(k) + '=' + str(v) + ', '
                    eval(f'{tile_class}(x, y, st.subsurface(pg.Rect({st_atlas[tile_data["tile"]][0]}, {st_atlas[tile_data["tile"]][1]}, plat_w, plat_h)), {kwargs_string})')
                case 'Text':
                    kwargs_string = ''
                    for k, v in tile_data.items():
                        if k in ['class', 'text', 'font', 'color']:
                            continue
                        kwargs_string += str(k) + '=' + str(v) + ', '
                    eval(f'{tile_class}(x, y, "{tile_data["text"]}", {tile_data["font"]}, {tile_data["color"]}, {kwargs_string})')
                case 'Checkpoint':
                    eval(f'{tile_class}(x, y)')

            x += plat_w
        y += plat_h
        x = 0
    
    if soft:
        entities.add(plr)

# Call this right away in main
def essential_init():
    global st, st_atlas
    st = load_image(rpath('resources/png/st.png'))
    with open(rpath('resources/png/st_atlas.json'), 'r') as f:
        st_atlas = loads(f.read())
        
def init(path):
    # Debug
    print('Loading map: ' + file_name(path))
    # End
    global plr, map_path, first_update, level_finished, frames_taken
    map_path = path

    # Clean up first
    level_finished = False
    frames_taken = 0
    entities.empty()
    objects.empty()

    set_main_variable('level_deaths', 0)

    load_map(path)
    plr = Player(plr_sx, plr_sy)

    first_update = True

def update():
    global plr, first_update
    global frames_taken, map_title, level_end_state, level_finished

    if level_finished:
        sfx_e.play(sfx_e_pos)
        music.fadeout(500)
        sleep(2)

        set_main_variable('level_frames_taken', frames_taken)
        set_main_variable('level_title', map_title)
        # Level deaths are appended upon death

        set_main_variable('game_just_finished', True)

        set_main_variable('render', level_end_state)
        set_main_variable('canClick', True)

    keys = pg.key.get_pressed()

    plr.update(keys)

    if first_update:
        music.play(rpath(map_track))
        first_update = False
    
    frames_taken += 1

def render(win):
    # calculate center
    o_x, o_y = width // 2 - plr.rect.x - plr_w // 2, height // 2 - plr.rect.y - plr_h // 2

    for m in misc:
        m.draw(win, offset=(o_x, o_y))
    for obj in objects:
        win.blit(obj.image, (obj.rect.x + o_x, obj.rect.y + o_y))
    for e in entities:
        if e.__class__.__name__ == 'Player': # Don't animate player if dead
            if dead:
                continue

        if isinstance(e, AnimatedSprite):
            e.animate()
            if hasattr(e, 'flipped'):
                if e.flipped:
                    e.image = pg.transform.flip(e.image, 1, 0)
        win.blit(e.image, (e.rect.x + o_x, e.rect.y + o_y))