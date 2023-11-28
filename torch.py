import pygame
import light
import interactable

class Torch(interactable.Interactable):
    def __init__(self, x, y):
        #super().__init__(x, y)

        # Set values based on the spritesheet
        self.frameWidth = 39
        self.frameHeight = 171

        self.sheet = pygame.image.load("Assets/Torch_Spritesheet.png").convert_alpha()
        self.sheet.set_clip(0, 0, self.frameWidth, self.frameHeight)
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #self.rect = pygame.Rect(x, y, 25, 75)

        #set up lit torch animation sequence
        self.frame = 0
        self.on_frames = { 0: (49, 0, self.frameWidth,  self.frameHeight), \
                              1: (0, 181, self.frameWidth,  self.frameHeight), \
                              2: (49, 181, self.frameWidth,  self.frameHeight), \
                            }

        self.range = pygame.Rect(x - self.rect.width/2, y - self.rect.height/2, self.rect.width*2, self.rect.height*2)

        #control animation speed
        self.time_counter = 0
        self.frame_timer = 5

        #self.color = (150, 50, 0)

        self.light = light.Light(self.rect.centerx, self.rect.centery, False)

    def get_frame(self, frame_set):

        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def draw(self, world, camera_x, camera_y):
        world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))

    def interact(self, player):
        #print(player)
        if self.interactable:
            self.light.refresh()
            player.light.refresh()
        #else:
        #    print("nothing should happen")

    def update(self):
        #update the light's state
        self.light.update(self.rect.centerx, self.rect.centery)

        #if the light has been recently attacked, it cannot be interacted with
        self.interactable = not self.light.attacked


        if self.light.alive:
            self.clip(self.on_frames)

            self.time_counter += 1
            if self.time_counter > self.frame_timer:
                self.time_counter = 0
                self.frame += 1
        else:
            self.clip((0, 0, 39, 171))

        self.image = self.sheet.subsurface(self.sheet.get_clip())
