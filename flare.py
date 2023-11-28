import pygame

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Flare():
    #pass position to
    def __init__(self, x, y, xdirection, ydirection):

        self.speed = 50
        self.direction = [0,0]

        magnitude = ((xdirection) ** 2 + (ydirection) ** 2) ** 0.5

        #normalize direction vector
        self.direction[0] = xdirection/magnitude
        self.direction[1] = ydirection/magnitude

        self.timerMax = 100
        self.timerCurrent = self.timerMax

        #for handling drawing
        self.max_radius = 500
        self.min_radius = 0


        self.max_light = 200
        self.min_light = 100

        self.frameWidth = 116
        self.frameHeight = 19

        self.sheet = pygame.image.load("Assets/Flare_Spritesheet.png").convert_alpha()
        self.sheet.set_clip(0, 0, self.frameWidth, self.frameHeight)
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.frame = 0
        self.on_frames = { 0: (0, 0, self.frameWidth,  self.frameHeight), \
                           1: (126, 0, self.frameWidth,  self.frameHeight), \
                            }

        #control animation speed
        self.time_counter = 0
        self.frame_timer = 3


        self.light_surface = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)

        self.current_radius = int((1.0 - self.timerCurrent/self.timerMax) * self.min_radius + self.timerCurrent/self.timerMax * self.max_radius)
        self.current_light = int((1.0 - self.timerCurrent/self.timerMax) * self.min_light + self.timerCurrent/self.timerMax * self.max_light)

        #pygame.draw.rect(self.light_surface, self.color, self.rect)
        pygame.draw.circle(self.light_surface, (0,0,0, self.current_light), (self.max_radius, self.max_radius), self.current_radius)



    def draw_flare(self, world, camera_x, camera_y):
        world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))

    def draw_light(self, darkness, camera_x, camera_y):
        draw_x = self.rect.centerx + camera_x
        draw_y = self.rect.centery + camera_y
        darkness.blit(self.light_surface, (draw_x - self.max_radius, draw_y - self.max_radius), special_flags = pygame.BLEND_RGBA_SUB)

    def moveX(self):
        self.rect.centerx += self.direction[0]*self.speed

    def collideHorizontal(self, wall):
        # handle flare X collision
        if self.direction[0] > 0:
            self.rect.right = wall.left
            #reverse direction but slow it down
            self.direction[0] = -self.direction[0]*0.5
        elif self.direction[0] < 0:
            self.rect.left = wall.right
            self.direction[0] = -self.direction[0]*0.5

        #if slow enough, set x direction to 0
        if abs(self.direction[0]) < 0.1:
            self.direction[0] = 0.0

    def moveY(self):
        #apply gravity
        self.direction[1] += 0.05
        #update y position
        self.rect.centery += self.direction[1]*self.speed

    def collideVertical(self, wall):
        # handle flare y collision
        if self.direction[1] > 0:
            self.rect.bottom = wall.top

            #let flare bounce, but slow it down
            self.direction[1] = -self.direction[1]*0.5
            #also, let flare x component slow down on a bounce
            self.direction[0] =  self.direction[0]*0.5

            #if slow enough, set x direction to 0
            if abs(self.direction[0]) < 0.1:
                self.direction[0] = 0.0
            #same with y direction:
            if abs(self.direction[1]) < 0.1:
                self.direction[1] = 0.0

        elif self.direction[1] < 0:
            self.rect.top = wall.bottom

            #let it bounce, no slow down
            self.direction[1] =  -self.direction[1]

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


    def update(self):

        if self.timerCurrent > 0:
            self.timerCurrent -= 1



        self.clip(self.on_frames)

        self.time_counter += 1
        if self.time_counter > self.frame_timer:
            self.time_counter = 0
            self.frame += 1
        self.image = self.sheet.subsurface(self.sheet.get_clip())


        self.current_radius = int((1.0 - self.timerCurrent/self.timerMax) * self.min_radius + self.timerCurrent/self.timerMax * self.max_radius)
        self.current_light = int((1.0 - self.timerCurrent/self.timerMax) * self.min_light + self.timerCurrent/self.timerMax * self.max_light)

        self.light_surface.fill((0, 0, 0, 0))
        #pygame.draw.rect(self.light_surface, self.color, self.rect)
        pygame.draw.circle(self.light_surface, (0,0,0, self.current_light), (self.max_radius, self.max_radius), self.current_radius)
