import pygame
import light

class Shadow():
    #pass initial position for rectangle here as x and y
    def __init__(self, x, y):

        self.x = x
        self.y = y

        #for drawing:
        self.radius = 300
        self.darkness_level = 230


        self.left = self.x - self.radius*2
        self.top = self.y - self.radius*2



        self.darkness_surface = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)

        pygame.draw.circle(self.darkness_surface, (0,0,0, self.darkness_level), (self.radius*2, self.radius*2), self.radius)


        #for AI
        self.hunting_radius = self.radius

        self.attack_radius = self.radius*2


        #when attacking, calculate direction to target, then mult by speed
        self.direction = [0,0]
        self.speed = 5

        # holds a reference to the light object it is targeting
        self.target = []


        #will be replaced by a sprite
        #self.attack = [] pygame.Rect(x-25, y, 50, self.radius*2)
        self.collsion_mask = pygame.mask.from_surface(self.darkness_surface)

        self.is_attacking = False

        # max of 50
        self.attack_cd = 0

        # max of 70
        self.dazed_timer = 0


        #bargain brand enum:
        # 0 = inactive
        # 1 = hunting
        # 2 = attacking
        # 3 = dazed
        self.state = 0
    def draw(self, darkness):
        self.darkness_surface.fill((0, 0, 0, 0))
        #DEBUG range
        if self.state == 1:
            pygame.draw.circle(self.darkness_surface, (0,0,0, self.darkness_level), (self.radius*2, self.radius*2), self.radius)
            pygame.draw.circle(self.darkness_surface, (255,0,0, 255), (self.radius*2, self.radius*2), self.hunting_radius, 2)
        elif self.state == 2:
            pygame.draw.circle(self.darkness_surface, (0,0,0, self.darkness_level), (self.radius*2, self.radius*2), self.radius)

        darkness.blit(self.darkness_surface, (self.x - self.radius*2, self.y - self.radius*2), special_flags = pygame.BLEND_RGBA_ADD)

    def update(self, light_list):
        if self.state == 1:
            self.hunt_ai(light_list)
        elif self.state == 2:
            self.attack_ai()
        elif self.state == 3:
            print("dazed")
        else:
            #print("inactive")\
            pass
        #if attack_cd not 0, attack_cd -= 1
        #

    def hunt_ai(self, light_list):
            #print("hunting")
            self.hunting_radius += 1
            distance = 0.0

            for light in light_list:
                if light.alive and self.state == 1:
                    #get the magnitude of the vector between the points
                    distance = ((light.x - self.x) ** 2 + (light.y - self.y) ** 2) ** 0.5
                    if distance <= self.hunting_radius:
                        self.target.append(light)
                        self.state = 2
                        self.hunting_radius = self.radius

    def attack_ai(self):
            #print("attacking", self.target)

            #first, check if our target is still alive:
            if not self.target[0].alive:
                self.target.pop()
                self.state = 1
            else:
                #find direction vector
                x_direction = self.target[0].x - self.x
                y_direction = self.target[0].y - self.y
                magnitude = ((x_direction) ** 2 + (y_direction) ** 2) ** 0.5


                #normalize direction vector
                self.direction[0] = x_direction/magnitude
                self.direction[1] = y_direction/magnitude


                #if we are far enough away, we want to move towards the target
                if(magnitude > self.radius * 0.75):
                    #travel in direction with a magnitude of speed
                    self.x += self.direction[0] * self.speed
                    self.y += self.direction[1] * self.speed


                ### NOTE: attack code will require an attack sprite sheet, which I don't have yet,
                ### so we'll deal with this later.

                #if we are close enough, we want to attack:
                #if(magnitude < self.attack_radius && attack_cd == 0)
                # attack()
                #   attack cd = 50
                #   attack.append (attack.spawn(x,y, direction))
