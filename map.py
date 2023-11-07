import pygame
import player
import torch
import shadow

class Map():
    def __init__(self):

        #overall map size
        self.width = 1600
        self.height = 1200
        self.world = pygame.Surface((self.width, self.height))

        #set up the alpha mask
        self.darkness_level = 210
        self.darkness_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)


        #replace this with a list of sprites based on a tilemap
        self.mapGeo = []
        #borders:
        self.mapGeo.append(pygame.Rect(0, 0, 1600, 50))
        self.mapGeo.append(pygame.Rect(0, 1150, 1600, 50))
        self.mapGeo.append(pygame.Rect(0, 50, 50, 1100))
        self.mapGeo.append(pygame.Rect(1550, 50, 50, 1100))

        #Low platform
        self.mapGeo.append(pygame.Rect(350, 850, 1000, 50))
        self.mapGeo.append(pygame.Rect(1400, 1000, 150, 50))

        #High platform
        self.mapGeo.append(pygame.Rect(350, 450, 1000, 50))

        #instantiate the Player
        self.player = player.Player(400, 400)

        #instantiate all interactable objects
        self.objects = []
        self.objects.append(torch.Torch(500, 375))
        self.objects.append(torch.Torch(1000, 375))
        self.objects.append(torch.Torch(500, 775))
        self.objects.append(torch.Torch(1000, 775))

        #instantiate the light list
        self.light_list = []
        self.light_list.append(self.player.light)
        for obj in self.objects:
            if obj.__class__.__name__ == "Torch":
                self.light_list.append(obj.light)

        #instantiate the Shadow
        self.shadow = shadow.Shadow(800, 0)

        #event flags for the map 3 states:
        # 0 = not spawned
        # 1 = set to spawn
        # 2 = already spawned
        self.spawn_shadow = 0

    def update(self, key):
        self.player.update(key, self.mapGeo, self.objects)

        for obj in self.objects:
            obj.update()

        #test monster ai script ,eventually flag will be manipulated by checking when the player picks up the key
        if key[pygame.K_m]:
            self.spawn_shadow = 1

        if self.spawn_shadow == 1:
            self.shadow.state = 1
            self.spawn_shadow = 2
        self.shadow.update(self.light_list)

        #handle collisions

        #monster attacks here

        #basic monster collision here:
        ###currently using distance, may change this to sprite collision later
        for light in self.light_list:
            distance = ((light.x - self.shadow.x) ** 2 + (light.y - self.shadow.y) ** 2) ** 0.5
            if(distance < self.shadow.radius and light.alive):
                light.lose_health(0.02)




    def draw(self):
        self.world.fill((99,102,106))
        for obj in self.mapGeo:
            pygame.draw.rect(self.world, (0, 0, 0), obj)
        for obj in self.objects:
            obj.draw(self.world)

        self.player.draw(self.world)

        #now, render lighting
        self.darkness_surface.fill((0, 0, 0, self.darkness_level))

        for light in self.light_list:
            light.draw(self.darkness_surface)

        self.shadow.draw(self.darkness_surface)

        self.world.blit(self.darkness_surface, (0,0))
