import pygame
import light

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Player():
    #pass initial position for rectangle here as x and y
    def __init__(self, x, y):
        self.walk_speed = 10
        self.jump_speed = 45

        self.x_max_speed = 20
        self.y_max_speed = 45

        self.gravity = 5
        self.can_jump = False

        self.x_vel = 0
        self.y_vel = 0

        #these will be replaced
        self.body = pygame.Rect(x, y, 50, 50)
        self.color = (245, 245, 220)

        #Player's light class instance
        self.light = light.Light(self.body.centerx, self.body.centery, True)

    #pass level geometry sprite group to this function, do collision detection in here.
    def update(self, key, mapGeo, objects):

        # UPDATES

        # check if the player was attacked recently, give them a speed buff if true
        if self.light.attacked:
            self.walk_speed = 15
            self.x_max_speed = 30
        else:
            self.walk_speed = 10
            self.x_max_speed = 20


        #EVENTS

        #INTERACTION/TEST
        if key[pygame.K_e]:
            for obj in objects:
                if self.body.colliderect(obj.range) and obj.interactable:
                    obj.interact(self)


        #testing light health mechanics
        if key[pygame.K_p]:
            self.light.lose_health(0.02)


        #MOVEMENT:
        ###messy, move collision detection out to map, inside a collision handler method (player move x, then check collision, player move y, then check collision)

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

        self.y_vel += self.gravity

        # Now, read input and move the character

        # Handle x component first

        if key[pygame.K_a]:
            self.x_vel -= self.walk_speed
        if key[pygame.K_d]:
            self.x_vel += self.walk_speed

        self.body.x += self.x_vel

        # now, check collisions on X, will get a bit weird for sprite groups
        if self.x_vel != 0:
            for wall in mapGeo:
                if self.body.colliderect(wall):
                    if self.x_vel > 0:
                        self.body.right = wall.left
                    elif self.x_vel < 0:
                        self.body.left = wall.right


        # Handle Y component next
        if key[pygame.K_SPACE] and self.can_jump:
            self.y_vel -= self.jump_speed
            self.can_jump = False
        #if key[pygame.K_w]:
        #    self.y_vel -= self.walk_speed
        #if key[pygame.K_s]:
        #    self.y_vel += self.walk_speed

        self.body.y += self.y_vel

        # now, check collisions on Y, will get a bit weird for sprite groups
        if self.y_vel != 0:
            for wall in mapGeo:
                if self.body.colliderect(wall):
                    if self.y_vel > 0:
                        self.body.bottom = wall.top
                        self.y_vel = 0
                        self.can_jump = True
                    elif self.y_vel < 0:
                        self.body.top = wall.bottom
                        self.y_vel = -self.gravity


        #update light now that player position is calculated
        self.light.update(self.body.centerx, self.body.centery)


    def draw(self, world):
        pygame.draw.rect(world, self.color, self.body)
