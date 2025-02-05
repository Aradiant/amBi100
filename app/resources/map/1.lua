a = require('actions')
ha = require('hit_actions')

hidden = a.hidden
hidden_hit = ha.hidden_hit

plr = '@'
nothing = ' '
level_end = "('+', 'Finish')"

title = 'Catasta dawn'
track = 'resources/ogg/mule.ogg'
max_jump_tick = 46

sinex_2 = [[
    '''
while self.alive():
    self.rect.x = self.x + math.sin(now()*1.5)*2*plat_w
    sleep(1/60)
    '''
]]
sinex_3 = [[
    '''
while self.alive():
    self.rect.x = self.x + math.sin(now()*3)*3*plat_w
    sleep(1/60)
    '''
]]
sinex_2_fast = [[
    '''
while self.alive():
    self.rect.x = self.x + math.sin(now()*2.5)*2*plat_w
    sleep(1/60)
    '''
]]

bullet_left = [[
    '''
cd = 0
while self.alive():
    if cd:
        cd -= 1

    self.rect.x -= 2
    sleep(1/60)
    temp = pg.sprite.spritecollide(sprite=self, group=objects, dokill=0)
    for t in temp:
        if t.__class__.__name__ == 'Platform':
            if t.image_name == 'st-plain':
                self.rect.x += 45 * 30
                cd = 3
                break
    '''
]]

bullet_left_alt = [[
    '''
cd = 0
while self.alive():
    if cd:
        cd -= 1

    self.rect.x -= 6
    sleep(1/60)
    temp = pg.sprite.spritecollide(sprite=self, group=objects, dokill=0)
    for t in temp:
        if t.__class__.__name__ == 'Platform':
            if t.image_name == 'st-flat':
                self.rect.x += 16 * 30
                cd = 3
                break
    '''
]]

data['o'] = {tile = 'st-border', class = 'Platform'}
data['#'] = {tile = 'st-plain', class = 'Platform'}
data['m'] = {tile = 'st-flat', class = 'Platform'}
data['M'] = {tile = 'st-flat-dark', class = 'Platform'}
data['b'] = {tile = 'st-crate', class = 'Platform'}
data['.'] = {tile = 'st-flat-ss', class = 'Platform'}
data[':'] = {tile = 'st-flat-s', class = 'Platform'}
data['-'] = {tile = 'st-bridge', class = 'Platform'}

data['1'] = {tile = 'st-spike-up', class = 'Platform', kills = true, action = sinex_2}
data['2'] = {tile = 'st-spike-up', class = 'Platform', kills = true, action = sinex_3}
data['3'] = {tile = 'st-hitbox-small', class = 'Platform', kills = true, action = bullet_left}
data['4'] = {tile = 'st-hitbox-small', class = 'Platform', kills = true, action = bullet_left_alt}
data['5'] = {tile = 'st-spike-up', class = 'Platform', kills = true, action = sinex_2_fast}

data['^'] = {tile = 'st-spike-up', class = 'Platform', kills = true}
data['v'] = {tile = 'st-spike-down', class = 'Platform', kills = true}
data['<'] = {tile = 'st-spike-left', class = 'Platform', kills = true}
data['>'] = {tile = 'st-spike-right', class = 'Platform', kills = true}

local text_color = '(145, 145, 145)'
data[']'] = {class = 'Text', text = 'Below you is only void.', font = 'font_pixel_16', color = text_color}

data['*'] = {class = 'Checkpoint'}

map = [[
^^^^^^                      2                      *                                                                                   
mmmmmm                   o-----o                 mmmmm          ^^^^^^   ^^^   ^ ^^^^^^^^                                              
######       .                          .        #####         mmmmmmm   mmm   mmmmmmmmmm    ^                     ^^^^^^^           ^^
######                                           #####         vvvvvvv     #            #   mmm                    M##m##M           mm
######  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#####                     #            # ^ ###          1            v              ##
######  mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm##### .               :   # o   ^      # m ###        o---o                         ##
######  ##############################################                     #     m      #   ###                    o     m           ##
######        3                    3                ##                     #     # ^    #   ###                          v           ##
######    3       3   3      3 3       3   3 3      ##   ^^^^^^ ^^^^^^^^^^^#   . # m#####> <###                            ^       mm##
##################################################  ##mmmmmmmmmmmmmmmmmmmmm#     #          ### @     ^  ^^^^^^^^  ^       m       ####
##################################################  ########################     #    * ^ * ###   ^   mmmmmmmmmmm  m     ^^M   ^   ####
######                    vv   MM                   ##################################################MM       MM######################
######                         mm 4                 ##################################################           ######################
######     ]   ^     ^               .      .       ##
######     *   m  5  m  ^^^^^^    ^^^^^^^^^^^^^^    ## +
######  ##############################################
######  ##############################################
##          ##                                     m  
##          ##                                     v  
## . ^^^^^^^##                  ^^                   .
##   mmmmmmmmm           :      mm                    
##          vv                  MM             .      
##              .               ##                    
##       :                      ##      :             
##                              ##                    
##                              ##                    
##                              ###                   
]]