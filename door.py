import pygame
import interactable

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Door(interactable.Interactable):
    def __init__(self, x, y, key_name):
        # Set values based on the spritesheet
        self.frameWidth = 265
        self.frameHeight = 440

        self.sheet = pygame.image.load("Assets/Door_Spritesheet.png").convert_alpha()
        #self.sheet = pygame.transform.flip(self.sheet, True, False)
        self.closedFrame = (0, 0, self.frameWidth, self.frameHeight)
        self.openFrame = (275, 0, self.frameWidth, self.frameHeight)
        self.sheet.set_clip(self.closedFrame)
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #special rect for collisions
        self.colliderect = pygame.Rect(self.rect.left, self.rect.top, 50, self.rect.height)

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        self.key_name = key_name

        self.interactable = True

    def draw(self, world, camera_x, camera_y):
        world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))

    def interact(self, player):
        if self.interactable:
            if self.key_name in player.inventory and player.inventory[self.key_name]:
                player.inventory[self.key_name] = False
                self.interactable = False

                self.sheet.set_clip(self.openFrame)
                self.image = self.sheet.subsurface(self.sheet.get_clip())
            else:
                print("the door is locked")

    def update(self):
        pass
