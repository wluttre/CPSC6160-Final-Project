import pygame
import interactable

class Key(interactable.Interactable):
    def __init__(self, x, y, name):
        #self.rect = pygame.Rect(x, y, 25, 25)
        self.image = pygame.image.load("Assets/Key_Sprite.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        self.key_name = name
        self.interactable = True

    def draw(self, world, camera_x, camera_y):
        if self.interactable:
            world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))

    def interact(self, player):
        if self.interactable:
            player.inventory[self.key_name] = True
            self.interactable = False
            #print(player.inventory)

    def update(self):
        pass
