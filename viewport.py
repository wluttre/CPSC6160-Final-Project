import pygame

class Viewport():
    def __init__(self, x, y, width, height):

        #overall map size
        self.width = width
        self.height = height

        #top left corner, will be based on player position
        self.x = x
        self.y = y

        self.view = pygame.Surface((self.width, self.height))

    def update_viewport(self, player_rect, map_width, map_height):

        #deltaX = abs(self.x) + self.width
        #deltaX -= player_rect.centerx

        #deltaY = abs(self.y) + self.height
        #deltaY -= player_rect.centery
        self.x = -(player_rect.centerx - self.width/2)
        self.y = -(player_rect.centery - self.height/2)

        if(self.x > 0):
            self.x = 0
        elif( abs(self.x) > map_width - self.width):
            self.x = -1*(map_width - self.width)

        if(self.y > 0):
            self.y = 0
        elif(abs(self.y) > map_height - self.height):
            self.y = -1*(map_height - self.height)

    def draw(self, world):
        self.view.fill((0,0,0))
        self.view.blit(world, (self.x, self.y))
        #print(self.x, ", ", self.y)
