# To replicate the Environment of virtual computing:
# Python 3.8.10
# Pygame 1.9.6
import pygame
import sys

import map
import viewport

pygame.init()

#This reflects viewport dimensions
screen_width    = 1280
screen_height   = 720

scale_factor = 0.5

unscaled_width = int(screen_width / scale_factor)
unscaled_height = int(screen_height / scale_factor)

screen = pygame.display.set_mode((screen_width, screen_height))

scaled_screen = pygame.Surface((unscaled_width, unscaled_height))

pygame.display.set_caption("CPSC 6160: Firelight")

#Initialize the map
map = map.Map(unscaled_width, unscaled_height)


view = viewport.Viewport(map.player.rect, unscaled_width, unscaled_height)

#set up refresh rate
clock = pygame.time.Clock()
#FPS = 60

#game loop boolean
game_over = False

while game_over == False:

    #GLOBAL EVENTS:

    #start by checking if player is alive, then end the game if they are not
    #NOTE: this should use another boolean and open an end of game screen
    #currently also the check for winning, this would open a separate winning screen
    game_over = not map.player.light.alive or map.win
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_over = True


    #because the mouse is "local" to the viewport, we must translate and scale to the world coordinates
    mouse_x = pygame.mouse.get_pos()[0] * 1/scale_factor + abs(view.x)
    mouse_y = pygame.mouse.get_pos()[1] * 1/scale_factor + abs(view.y)
    map.update(pygame.key.get_pressed(), events, (mouse_x, mouse_y))
    view.update_viewport(map.player, map.width, map.height, 1)


    #DRAWING:

    screen.fill((255,255,255))
    map.draw(scaled_screen, view.x,  view.y)
    new_screen = pygame.transform.scale(scaled_screen,(int(screen_width), int(screen_height)))

    screen.blit(new_screen, (0,0))
    #this scales the world to draw everything smaller
    #scaled_world = pygame.transform.scale(map.world,(int(map.width*scale_factor), int(map.height*scale_factor)))

    view.draw(screen)
    #view.draw(map.world)
    #screen.blit(view.view, (0, 0))
    pygame.display.flip()
    clock.tick(25)

pygame.quit()
sys.exit()
