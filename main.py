# To replicate the Environment of virtual computing:
# Python 3.8.10
# Pygame 1.9.6
import pygame
import sys

import map
import viewport

pygame.init()

#This reflects viewport dimensions
screen_width    = 1000
screen_height   = 450

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CPSC 6160: Firelight")

#Initialize the map
map = map.Map()


view = viewport.Viewport(map.player.body.x, map.player.body.y, screen_width, screen_height)

#set up refresh rate
clock = pygame.time.Clock()
#FPS = 60

#game loop boolean
game_over = False

while game_over == False:

    #GLOBAL EVENTS:

    #start by checking if player is alive, then end the game if they are not
    #NOTE: this should use another boolean and open an end of game screen
    game_over = not map.player.light.alive

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True


    #EVENT/UPDATES:
    #this input code will be handled by map.update() later
#    key = pygame.key.get_pressed()
#    deltaX = 0
#    deltaY = 0

#    if key[pygame.K_a]:
#        deltaX += 10
#    if key[pygame.K_d]:
#        deltaX -= 10
#    if key[pygame.K_w]:
#        deltaY += 10
#    if key[pygame.K_s]:
#        deltaY -= 10

    map.update(pygame.key.get_pressed())
    view.update_viewport(map.player.body, map.width, map.height)


    #DRAWING:

    screen.fill((255,255,255))
    map.draw()
    view.draw(map.world)
    screen.blit(view.view, (0, 0))
    pygame.display.flip()
    clock.tick(25)

pygame.quit ()
sys.exit()
