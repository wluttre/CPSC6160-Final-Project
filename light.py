import pygame

#this will eventually extend sprite. Right now, it will just have a rectangle for collisions
class Light():
    #pass position to
    def __init__(self, x, y, isAlive):

        self.x = x
        self.y = y

        self.alive = isAlive

        self.attacked = False
        self.attack_CD = 0.0

        #for handling drawing
        self.max_radius = 200
        self.min_radius = 50


        self.max_light = 200
        self.min_light = 100

        #for handling health
        if self.alive:
            self.health = 1.0
        else:
            self.health = 0.0


        self.light_surface = pygame.Surface((self.max_radius*2, self.max_radius*2), pygame.SRCALPHA)

        self.current_radius = int((1.0 - self.health) * self.min_radius + self.health * self.max_radius)
        self.current_light = int((1.0 - self.health) * self.min_light + self.health * self.max_light)

        pygame.draw.circle(self.light_surface, (0,0,0, self.current_light), (self.max_radius, self.max_radius), self.current_radius)




    def draw(self, darkness):
        if self.alive:
            darkness.blit(self.light_surface, (self.x - self.max_radius, self.y - self.max_radius), special_flags = pygame.BLEND_RGBA_SUB)

    def refresh(self):
        self.health  = 1.0
        self.current_radius = int((1.0 - self.health) * self.min_radius + self.health * self.max_radius)
        self.current_light = int((1.0 - self.health) * self.min_light + self.health * self.max_light)

        self.light_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.light_surface, (0,0,0, self.current_light), (self.max_radius, self.max_radius), self.current_radius)

        self.alive = True

    def lose_health(self, hp_loss):
        self.health -= hp_loss

        self.attacked = True
        self.attack_CD = 50

        self.current_radius = int((1.0 - self.health) * self.min_radius + self.health * self.max_radius)
        self.current_light = int((1.0 - self.health) * self.min_light + self.health * self.max_light)

        self.light_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(self.light_surface, (0,0,0, self.current_light), (self.max_radius, self.max_radius), self.current_radius)

        if self.health <= 0:
            self.health = 0.0
            self.alive = False


    def update(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

        #if a light has been attacked, it has different state behavior for a certain time
        # for the player, their move speed is increased
        # for a torch, they cannot be refreshed by the player
        if self.attacked:
            self.attack_CD -= 1
            if self.attack_CD <= 0:
                self.attack_CD = 0
                self.attacked = False
