-- Collection of generic hit actions
-- Platform is referred to as c_sprite, player object is self
-- (this is because the code runs inside the player class upon collision)

return {

hidden_hit = [['''

if c_sprite.hidden:
    c_sprite.hidden = False
    if getattr(c_sprite, 'kills', False) == False:
        sfx_obj.play(sfx_reveal)
    else:
        sfx_obj.play(sfx_deadlyreveal)
    c_sprite.image.set_alpha(255)

''']]

}