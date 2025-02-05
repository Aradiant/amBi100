a = require('actions')
ha = require('hit_actions')

hidden = a.hidden
hidden_hit = ha.hidden_hit

plr = '@'
nothing = ' '
level_end = "('+', 'Finish')"

title = 'Oort train'
track = 'resources/ogg/artcorehidden.ogg'
max_jump_tick = 46

sinex_10_fast = [[
    '''
while self.alive():
    self.rect.x = self.x + math.sin(now()*2.5)*10*plat_w
    sleep(1/60)
    '''
]]
sinex_10_fast_reverse = [[
    '''
while self.alive():
    self.rect.x = self.x - math.sin(now()*2.5)*10*plat_w
    sleep(1/60)
    '''
]]
sinexsq_12_fast = [[
    '''
while self.alive():
    self.rect.x = self.x + (math.sin(now()*2)**2)*10*plat_w
    sleep(1/60)
    '''
]]
sinexsq_20_fast = [[
    '''
while self.alive():
    self.rect.x = self.x + abs(math.sin(now()*1.45))*10*2*plat_w
    sleep(1/60)
    '''
]]
sinexsq_20_fast_reverse = [[
    '''
while self.alive():
    self.rect.x = self.x - abs(math.sin(now()*1.45))*10*2*plat_w
    sleep(1/60)
    '''
]]
move_1_down = [[
    '''
    self.rect.y = self.y + plat_h
    '''
]]
follow_20_right = [[
    '''
global read_only_plr_x
while self.alive():
    self.rect.x = clamp(read_only_plr_x, self.x, self.x + plat_w*20)
    sleep(1/60)
    '''
]]
complex_pattern = [[
    '''
while self.alive():
    self.rect.x = self.x + math.sin(now()*5)*1.25*plat_w
    self.rect.y = self.y + (math.sin(now()*0.9))**2*19*plat_h
    sleep(1/60)
    '''
]]
sinex1 = [[
    '''
while self.alive():
    self.rect.x = self.x - math.sin(now())**5*0.4*plat_w
    sleep(1/60)
    '''
]]

data['o'] = {tile = 'st-border', class = 'Platform'}
data['#'] = {tile = 'st-brick', class = 'Platform'}
data['='] = {tile = 'st-slate', class = 'Platform'}
data['-'] = {tile = 'st-bridge', class = 'Platform'}

data['^'] = {tile = 'st-spike-up', class = 'Platform', kills = true}
data['v'] = {tile = 'st-spike-down', class = 'Platform', kills = true}
data['<'] = {tile = 'st-spike-left', class = 'Platform', kills = true}
data['>'] = {tile = 'st-spike-right', class = 'Platform', kills = true}

data['!'] = {tile = 'st-spike-up', class = 'Platform', kills = true, action = hidden, hit_action = hidden_hit}

local text_color = '(145, 145, 145)'
local u_text_color = '(45, 45, 45)'
data['['] = {class = 'Text', text = 'This is a double jump replenisher.', font = 'font_pixel_16', color = text_color}
data[']'] = {class = 'Text', text = 'Note that it is always consumed on touch.', font = 'font_pixel_16', color = text_color, oy = -15}
data['{'] = {class = 'Text', text = 'That was far too easy...', font = 'font_pixel_16', color = u_text_color}
data['}'] = {class = 'Text', text = 'Does it say \'\'gullible\'\' on the ceiling?', font = 'font_pixel_16', color = text_color}
data['|'] = {class = 'Text', text = 'Work in progress.', font = 'font_pixel_16', color = text_color, oy=25}

data['.'] = {tile = 'st-flat-ss', class = 'Platform'}

data['1'] = {class = 'Platform', kills = true, tile = 'st-hitbox-small', action = sinex_10_fast}
data['2'] = {class = 'Platform', kills = true, tile = 'st-hitbox-small', action = sinex_10_fast_reverse}
data['3'] = {class = 'Platform', kills = true, tile = 'st-spike-up', action = sinexsq_20_fast}
data['4'] = {class = 'Platform', kills = true, tile = 'st-spike-up', action = sinexsq_20_fast_reverse}
data['5'] = {class = 'Platform', tile = 'st-slate', action = follow_20_right}
data['6'] = {class = 'Platform', kills = true, tile = 'st-spike-down', action = follow_20_right}
data['7'] = {class = 'Platform', kills = true, tile = 'st-hitbox-small', action = complex_pattern}
data['8'] = {class = 'Platform', kills = true, tile = 'st-hitbox-small', action = sinex1}
data[';'] = {class = 'Platform', kills = true, tile = 'st-spike-up', action = move_1_down}

data['*'] = {class = 'Checkpoint'}
data['J'] = {class = 'JumpRestore'}

map = [[
#############
#############
##    |    ##
##    @    ##
##         ##
#############
#############
]]