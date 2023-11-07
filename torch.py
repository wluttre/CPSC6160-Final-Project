import pygame
import light
import interactable

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Torch(interactable.Interactable):
    def __init__(self, x, y):
        #super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 25, 75)

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        self.color = (150, 50, 0)

        self.light = light.Light(self.rect.centerx, self.rect.centery, False)

    def draw(self, world):
        pygame.draw.rect(world, self.color, self.rect)

    def interact(self, player):
        #print(player)
        if self.interactable:
            self.light.refresh()
            player.light.refresh()
        else:
            print("nothing should happen")

    def update(self):
        #update the light's state
        self.light.update(self.rect.centerx, self.rect.centery)

        #if the light has been recently attacked, it cannot be interacted with
        self.interactable = not self.light.attacked
