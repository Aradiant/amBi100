a = require('actions')
ha = require('hit_actions')

hidden = a.hidden
hidden_hit = ha.hidden_hit

plr = '@'
nothing = ' '
level_end = "('+', 'Finish')"

title = 'Tutorial'
track = 'resources/ogg/ambi254.ogg'

data['o'] = {tile = 'st-border', class = 'Platform'}
data['-'] = {tile = 'st-bridge', class = 'Platform'}
data['_'] = {tile = 'st-bridge-low', class = 'Platform'}
data['#'] = {tile = 'st-brick', class = 'Platform'}
data['m'] = {tile = 'st-tile', class = 'Platform'}
data['b'] = {tile = 'st-crate-dark', class = 'Platform'}

data['?'] = {tile = 'st-metal', class = 'Platform', action = hidden, hit_action = hidden_hit}

data['^'] = {tile = 'st-spike-up', class = 'Platform', kills = true}
data['!'] = {tile = 'st-spike-up', class = 'Platform', kills = true, action = hidden, hit_action = hidden_hit}

data['*'] = {class = 'Checkpoint'}

local u_text_color = '(85, 85, 85)'
local text_color = '(145, 145, 145)'
local h_text_color = '(185, 185, 185)'
data['1'] = {class = 'Text', text = 'Welcome to amBi100.', font = 'font_pixel_16_bold', color = h_text_color}
data['2'] = {class = 'Text', text = 'Use arrow keys to perform horizontal movement.', font = 'font_pixel_16', color = text_color}
data['3'] = {class = 'Text', text = 'Press S to perform a jump.', font = 'font_pixel_16', color = text_color}
data['4'] = {class = 'Text', text = 'Holding S results in a higher jump.', font = 'font_pixel_16', color = text_color}
data['5'] = {class = 'Text', text = 'Press S while airborne to perform a double jump.', font = 'font_pixel_16', color = text_color}
data['6'] = {class = 'Text', text = 'This is a checkpoint.', font = 'font_pixel_16_bold', color = h_text_color}
data['7'] = {class = 'Text', text = 'You can guess what happens', font = 'font_pixel_16', color = text_color}
data['8'] = {class = 'Text', text = 'if you fall down.', font = 'font_pixel_16', color = text_color}
data['9'] = {class = 'Text', text = 'Press R to reset.', font = 'font_pixel_16', color = text_color}
data['0'] = {class = 'Text', text = 'Memorize traps.', font = 'font_pixel_16', color = text_color}
data['&'] = {class = 'Text', text = 'Hold A to walk.', font = 'font_pixel_16', color = text_color}
data['z'] = {class = 'Text', text = 'Lastly, pressing Z allows you to see more.', font = 'font_pixel_16', color = text_color}
data['Z'] = {class = 'Text', text = 'Use it to get as much advantage as possible.', font = 'font_pixel_16_bold', color = h_text_color}
data['.'] = {class = 'Text', text = 'And remember:', font = 'font_pixel_16', color = text_color}
data['~'] = {class = 'Text', text = 'This isn\'t everything you\'ll see later.', font = 'font_pixel_16_bold', color = h_text_color}
data['G'] = {class = 'Text', text = 'Good luck.', font = 'font_pixel_16_bold', color = h_text_color}
data['}'] = {class = 'Text', text = 'If you ever want to return to the menu from a level, use the \'\'Close window\'\' button.', font = 'font_pixel_8', color = u_text_color, oy = -15}

map = [[
############################################################
############################################################
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                        ##
##                                                    ##  ##
##                                                    ##  ##
##                                            5       ##  ##
##                                4                   ##  ##
##                       3             #################  ##
##           @                         #################  ##
##                            ########################    ##
##----------------------------########################    ##
##           1                ####################      ####
##           2                ####################      ####
##                            ####################    ######
##                            ####################    ######
##                            ####################b     ####
##                            ####################bb    ####
##^^^^^^^^^^^^^^^^^^^^^^^^^^^^########################    ##
######################################################    ##
################################mmmmmmmmmmm#############  ##
################################m         m#############  ##
################################m    7    m#############  ##
##           ##                      8           6        ##
##           ##                                  *       b##
## ???##---- ##     #####     #####m   m######-------#######
##    ##     ##     #####     #####m^^^m######       #######
##    ##     ##     #####     #####mmmmm######       #######
##    ## ____##     #####     ################       #######
##??? ##          bb#####     ################       #######
##    ##        bbbb#####     ################       #######
##    ###################     ################       #######
##    ###################  9  ################       #######
## ???###################mmmmm################       #######
##          ???                    mmmmmmm                ##
##                                              ^^^       ##
##    0             ^^                &         mmm       ##
##    *     ^^^     mm     !   *   ^ ^ ^ ^      mmm   ^^  ##
########################################################  ##
########################################################  ##
######################################################    ##
###mmmmm##############################################    ##
###m   m##############################################  ####
###m + m##############################################  ####
##                                                      ####
##                                                      ####
##b                         .             z             ####
##bb           G            ~             Z           bb####
##bbbb                                              bbbb####
#########----------------------------------------###########
#########      }                                 ###########
#########^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^###########
############################################################
############################################################
]]