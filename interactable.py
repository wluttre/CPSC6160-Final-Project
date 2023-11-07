import pygame

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Interactable():
    #pass initial position for rectangle here as x and y
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        self.color = (0, 255, 0)

        self.interactable = True

    def draw(self, world):
        pygame.draw.rect(world, (0,0,255), self.range)
        pygame.draw.rect(world, self.color, self.rect)

    def interact(self, player):
        if self.interactable:
            print("click")
            self.interactable = False
        else:
            print("nothing should happen")
    def update(self):
        pass
