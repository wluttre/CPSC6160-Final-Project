import pygame
import ui
class Viewport():
    def __init__(self, player_rect, width, height):

        #overall map size
        self.width = width
        self.height = height

        self.x = player_rect.centerx
        self.y = player_rect.centery

        self.view = pygame.Surface((self.width, self.height))

        self.ui = ui.UI(10, 10, 0.5)

    def update_viewport(self, player, map_width, map_height, scale_factor):

        self.x = -(player.rect.centerx - self.width/2)
        self.y = -(player.rect.centery - self.height/2)

        # to scale the map, need to scale viewport movement like this, scale factor of 0.5
        inverted_scale = 1/scale_factor
        self.x = -(player.rect.centerx - self.width/2 * inverted_scale)*scale_factor
        self.y = -(player.rect.centery - self.height/2 * inverted_scale)*scale_factor

        if self.x > 0:
            self.x = 0
        elif abs(self.x) > (map_width * scale_factor - self.width):
            self.x = -1*(map_width * scale_factor - self.width)

        if(self.y > 0):
            self.y = 0
        elif abs(self.y) > (map_height * scale_factor - self.height):
            self.y = -1*(map_height * scale_factor - self.height)

        has_key = "door_key" in player.inventory and player.inventory["door_key"]
        self.ui.update(player.light.health, player.inventory["Flares"], has_key)

    def draw(self, screen):
        #self.view.fill((0,0,0))
        #self.view.blit(world, (self.x, self.y))
        self.ui.draw(screen)
        #print(self.x, ", ", self.y)
