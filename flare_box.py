import pygame
import interactable

class FlareBox(interactable.Interactable):
    def __init__(self, x, y, flares):
        self.image = pygame.image.load("Assets/Flare_Box_Sprite.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        self.interactable = True
        self.flare_count = flares

    def draw(self, world, camera_x, camera_y):
        if self.interactable:
            world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))

    def interact(self, player):
        if self.interactable:
            player.inventory["Flares"] += self.flare_count
            self.interactable = False
            print("you got ", self.flare_count, " flares.")

    def update(self):
        pass
