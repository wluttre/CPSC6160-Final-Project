import pygame
import light
import flare

class Player(pygame.sprite.Sprite):
    #pass initial position for rectangle here as x and y
    def __init__(self, x, y):
        self.walk_speed = 20
        self.jump_speed = 300

        self.x_max_speed = 40
        self.y_max_speed = 45

        self.gravity_rate = 0.25
        self.gravity = 1
        self.can_jump = False

        self.x_vel = 0
        self.y_vel = 0


        self.frameWidth = 301
        self.frameHeight = 393

        self.sheet = pygame.image.load("Assets/Player_Spritesheet_ver02.png").convert_alpha()
        self.sheet.set_clip(0, 0, self.frameWidth, self.frameHeight)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.frame = 0
        self.facing_right = False
        self.throwing_flare = False

        self.walk_frames = { 0: (0, 0, self.frameWidth,  self.frameHeight), \
                              1: (311, 0, self.frameWidth,  self.frameHeight), \
                            }
        self.throw_frames = { 0: (0, 403, self.frameWidth,  self.frameHeight), \
                              1: (311, 403, self.frameWidth,  self.frameHeight), \
                            }

        #control animation speed
        self.time_counter = 0
        self.frame_timer = 5

        #Player's light class instance
        self.light = light.Light(self.rect.centerx, self.rect.centery, True)

        #Player's inventory
        self.inventory = {"Flares": 1}
        self.activeFlares = []

    def decaySpeed(self):
        #handle speed decay and max speed for X here.
        if(self.x_vel > 0):
            if(abs(self.x_vel) > self.x_max_speed):
                self.x_vel = self.x_max_speed
            self.x_vel -= self.walk_speed
            if(self.x_vel < 0):
                self.x_vel = 0

        elif(self.x_vel < 0):
            if(abs(self.x_vel) > self.x_max_speed):
                self.x_vel = -self.x_max_speed
            self.x_vel += self.walk_speed
            if(self.x_vel > 0):
                self.x_vel = 0


        #Y doesn't have to worry about speed decay, instead, we always subtract gravity
        if(self.y_vel > 0):
            if(abs(self.y_vel) > self.y_max_speed):
                self.y_vel = self.y_max_speed
            self.can_jump = False

        elif(self.y_vel < 0):
            if(abs(self.y_vel) > self.y_max_speed):
                self.y_vel = -self.y_max_speed


    #direction is either +1 or -1
    def moveX(self, direction):
        if not self.throwing_flare:
            self.x_vel += self.walk_speed * direction

    def collideHorizontal(self, wall):
        # handle player X collision
        if self.x_vel > 0:
            self.rect.right = wall.left
        elif self.x_vel < 0:
            self.rect.left = wall.right

    def jump(self):
        if not self.throwing_flare:
            self.y_vel -= self.jump_speed
            self.can_jump = False

    def moveY(self):
        if not self.can_jump:
            self.gravity += self.gravity_rate
        else:
            self.gravity = 2
        self.y_vel += self.gravity

    def collideVertical(self, wall):
        if self.y_vel > 0:
            self.rect.bottom = wall.top
            self.y_vel = 0
            self.can_jump = True
        elif self.y_vel < 0:
            self.rect.top = wall.bottom
            self.y_vel = -self.gravity

    #while throwing a flare, the player should not be able to move,until the animation is finished
    def throwFlare(self, mouse_position):
        if self.inventory["Flares"] > 0:
            if self.can_jump and not self.throwing_flare:
                #first, calculate the direction vector from the player and the mouse position
                ### need to multiply mouse position by scaling factor to calculate this correctly
                x_direction = mouse_position[0] - self.rect.centerx
                y_direction = mouse_position[1] - self.rect.centery
                magnitude = ((x_direction) ** 2 + (y_direction) ** 2) ** 0.5
                x_direction = x_direction/magnitude
                y_direction = y_direction/magnitude
                self.activeFlares.append(flare.Flare(self.rect.centerx, self.rect.centery, x_direction, y_direction))
                self.inventory["Flares"] -= 1
                #set animation information:
                if x_direction < 0:
                    self.facing_right = False
                else:
                    self.facing_right = True
                self.throwing_flare = True
                self.frame = 0
        else:
            print("no flares left.")

    def useFlare(self):
        if(self.inventory["Flares"] > 0):
            if self.can_jump and not self.throwing_flare:
                self.light.refresh()
                self.inventory["Flares"] -= 1
        else:
            print("no flares left.")



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
        # check all flares to see if the need to be deleted
        new_flares = []
        for f in self.activeFlares:
            f.update()
            if f.timerCurrent > 0:
                new_flares.append(f)
        self.activeFlares = new_flares

        # check if the player was attacked recently, give them a speed buff if true
        if self.light.attacked:
            self.walk_speed = 30
            self.x_max_speed = 60
        else:
            self.walk_speed = 20
            self.x_max_speed = 40


        #update light now that player position is calculated
        self.light.update(self.rect.centerx, self.rect.centery)

        # update the animation frame:
        # walking:
        if not self.throwing_flare:
            if self.x_vel > 0:
                self.facing_right = True
                self.clip(self.walk_frames)

                self.time_counter += 1
                if self.time_counter > self.frame_timer:
                    self.time_counter = 0
                    self.frame += 1
            elif self.x_vel < 0:
                self.facing_right = False
                self.clip(self.walk_frames)
                self.time_counter += 1
                if self.time_counter > self.frame_timer:
                    self.time_counter = 0
                    self.frame += 1

        #if we're throwing a flare, do that instead
        else:
                self.clip(self.throw_frames)

                self.time_counter += 1
                if self.time_counter > self.frame_timer:
                    self.time_counter = 0
                    self.frame += 1
                    if self.frame > (len(self.throw_frames) - 1):
                        self.frame = 1
                        self.throwing_flare = False
                        self.clip(self.walk_frames[0])
        #else:
            #if not moving, then go back to the first frame of the walk cycle
            #self.frame = 0
            #self.time_counter = 0
            #self.clip(self.walk_frames)

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def draw(self, world, camera_x, camera_y):
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        world.blit(self.image, (self.rect.left + camera_x, self.rect.top + camera_y))
        #pygame.draw.rect(world, (255, 0, 0), self.rect)
