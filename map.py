import pygame
import player
import torch
import key
import door
import shadow
import map_layout
import flare_box

class Map():
    def __init__(self, screen_width, screen_height):

        #overall map size
        self.width = 512 * 10
        self.height = 512 * 10
        #self.world = pygame.Surface((self.width, self.height))

        #set up the alpha mask #210, pretty bright
        self.darkness_level = 235
        #self.darkness_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.darkness_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


        # set up map geometry
        self.mapGeo2 = map_layout.MapLayout(self.width, self.height)

        #holds collision information from the map and doors
        self.collisionSet = self.mapGeo2.collisionSet

        #instantiate the Player
        self.player = player.Player(400, 830)

        #instantiate all interactable objects
        self.objects = []
        self.objects.append(torch.Torch(768, 902))
        self.objects.append(torch.Torch(2048, 390))
        self.objects.append(torch.Torch(512, 2440))
        self.objects.append(torch.Torch(2560, 2440))
        self.objects.append(key.Key(3372, 1576, "door_key"))

        new_door = door.Door(200, 2300, "door_key")
        self.objects.append(new_door)

        self.collisionSet.append(new_door.colliderect)
        self.objects.append(flare_box.FlareBox(850, 1090, 10))
        self.objects.append(flare_box.FlareBox(1800, 570, 2))

        #instantiate the light list
        self.light_list = []
        self.light_list.append(self.player.light)
        for obj in self.objects:
            if obj.__class__.__name__ == "Torch":
                self.light_list.append(obj.light)

        #instantiate the Shadow
        self.shadow = shadow.Shadow(4500, 2000)

        #event flag for the map. 3 states:
        # 0 = not spawned
        # 1 = set to spawn
        # 2 = already spawned
        self.spawn_shadow = 0

        self.win = False

    def update(self, key, events, mouse_world_pos):

        for obj in self.objects:
            obj.update()

        # INPUTS
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #self.player.throwFlare(pygame.mouse.get_pos())
                self.player.throwFlare(mouse_world_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.player.useFlare()

            #INTERACTION/TEST
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                for obj in self.objects:
                    if self.player.rect.colliderect(obj.range) and obj.interactable:
                        obj.interact(self.player)
                        if not obj.interactable and type(obj) is door.Door:
                            self.collisionSet.remove(obj.colliderect)


        self.player.decaySpeed()
        # Move player X
        if key[pygame.K_a]:
            self.player.moveX(-1)
        if key[pygame.K_d]:
            self.player.moveX(1)

        self.player.rect.x += self.player.x_vel

        # handle player X collision
        #for wall in self.mapGeo2.collisionSet:
        #    if self.player.rect.colliderect(wall):
        #        self.player.collideHorizontal(wall)
        collision = self.player.rect.collidelist(self.mapGeo2.collisionSet)

        if collision != -1:
            self.player.collideHorizontal(self.mapGeo2.collisionSet[collision])


        # Move player Y
        if key[pygame.K_SPACE] and self.player.can_jump:
            self.player.jump()

        self.player.moveY()

        self.player.rect.y += self.player.y_vel

        #handle player Y collision
        #for wall in self.mapGeo2.collisionSet:
        #    if self.player.rect.colliderect(wall):
        #        self.player.collideVertical(wall)
        collision = self.player.rect.collidelist(self.mapGeo2.collisionSet)

        if collision != -1:
            self.player.collideVertical(self.mapGeo2.collisionSet[collision])

        #now, update the player once the final position is decided
        self.player.update()

        #now, update flares:
        for flare in self.player.activeFlares:
            flare.moveX()

            collision = flare.rect.collidelist(self.mapGeo2.collisionSet)

            if collision != -1:
                flare.collideHorizontal(self.mapGeo2.collisionSet[collision])

            #for wall in self.mapGeo2.collisionSet:
            #    if flare.rect.colliderect(wall):
            #        flare.collideHorizontal(wall)

            flare.moveY()
            #for wall in self.mapGeo2.collisionSet:
            #    if flare.rect.colliderect(wall):
            #        flare.collideVertical(wall)

            collision = flare.rect.collidelist(self.mapGeo2.collisionSet)

            if collision != -1:
                flare.collideVertical(self.mapGeo2.collisionSet[collision])


        #now, check if the shadow is colliding with any active flares
            if self.shadow.state == 1 or self.shadow.state == 2:
                distance = ((flare.rect.centerx - self.shadow.x) ** 2 + (flare.rect.centery - self.shadow.y) ** 2) ** 0.5
                if distance <= self.shadow.radius:
                    self.shadow.state = 3
                    self.shadow.dazed_timer = 70


        #test monster ai script ,eventually flag will be manipulated by checking when the player picks up the key
        #if key[pygame.K_m]:
        if "door_key" in self.player.inventory:
            self.spawn_shadow += 1

        #testing player light health mechanics
        if key[pygame.K_p]:
            self.player.light.lose_health(0.02)

        if self.spawn_shadow == 1:
            self.shadow.state = 1
            self.spawn_shadow = 2
        self.shadow.update(self.light_list)

        #handle collisions

        #monster attacks here
        #basic monster collision here:
        ###currently using distance, may change this to sprite collision later
        if self.shadow.state == 2:
            for light in self.light_list:
                distance = ((light.x - self.shadow.x) ** 2 + (light.y - self.shadow.y) ** 2) ** 0.5
                if(distance < self.shadow.radius and light.alive):
                    light.lose_health(0.02)

        if self.player.rect.x < 0:
            self.win = True
            print("you win!")



    def draw(self,screen, camera_x, camera_y):
        #self.world.fill((43,44,90))
        screen.fill((43,44,90))
        #self.mapGeo2.draw(self.world)
        self.mapGeo2.draw(screen, camera_x, camera_y)

        #for obj in self.objects:
        #    obj.draw(self.world)

        for obj in self.objects:
            obj.draw(screen, camera_x, camera_y)

        #self.player.draw(self.world)
        self.player.draw(screen, camera_x, camera_y)

        #now, render lighting
        self.darkness_surface.fill((0, 0, 0, self.darkness_level))

        for light in self.light_list:
            light.draw(self.darkness_surface, camera_x, camera_y)

        self.shadow.draw(self.darkness_surface, camera_x, camera_y)

        for flare in self.player.activeFlares:
            #flare.draw_flare(self.world)
            flare.draw_flare(screen, camera_x, camera_y)
            flare.draw_light(self.darkness_surface, camera_x, camera_y)


        #self.world.blit(self.darkness_surface, (0,0))
        screen.blit(self.darkness_surface, (0, 0))
        print(camera_x, camera_y)
