import pygame
import csv

# currently loads both the game's tilesets here to be used by map.py,
# instead, doing this through a json file or inherited classes might be more extensible
class MapLayout(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height):
        self.width = map_width
        self.height = map_height
        #constant value based on tileset
        self.tileSize = 512
        self.mapSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.bgTileset = pygame.image.load("Assets/BG_Tileset.png").convert_alpha()
        self.fgTileset = pygame.image.load("Assets/FG_Tileset.png").convert_alpha()

        #self.bgTileset.set_clip(pygame.Rect(0,0,self.tileSize,self.tileSize))
        self.bgTileDict = { "CenterWindow":  (0, 0, 512, 512), \
                            "Center":        (522, 0, 512, 512), \
                            "Right":         (1044, 0, 512, 512), \
                            "Left":          (1566, 0, 512, 512), \
                            "Top":           (2088, 0, 512, 512), \
                            "Bottom":         (0, 522, 512, 512), \
                            "Bottom Right":   (522, 522, 512, 512), \
                            "Bottom Left":    (1044, 522, 512, 512), \
                            "Top Right":      (1566, 522, 512, 512), \
                            "Top Left":       (2088, 522, 512, 512), \
                          }

        self.fgTileDict = { "2WayH":  ((0, 0, 512, 512), 0), \
                            "2WayV":  ((0, 0, 512, 512), 90), \
                            "4Way":        ((522, 0, 512, 512), 0), \
                            "1WayLeft":        ((1044, 0, 512, 512), 0), \
                            "1WayDown":        ((1044, 0, 512, 512), 90), \
                            "1WayRight":        ((1044, 0, 512, 512), 180), \
                            "1WayUp":        ((1044, 0, 512, 512), 270), \
                            "3WayUp":        ((0, 522, 512, 512), 0), \
                            "3WayLeft":        ((0, 522, 512, 512), 90), \
                            "3WayDown":        ((0, 522, 512, 512), 180), \
                            "3WayRight":        ((0, 522, 512, 512), 270), \
                            "2WayBR":        ((522, 522, 512, 512), 0), \
                            "2WayTR":        ((522, 522, 512, 512), 90), \
                            "2WayTL":        ((522, 522, 512, 512), 180), \
                            "2WayBL":        ((522, 522, 512, 512), 270), \
                          }


        #list that will contain all background tiles
        self.bgTiles = []

        #list that contains all foreground tiles and collision data
        self.fgTiles = []
        self.collisionSet = []

        self.setMapGeo()

    #map dimensions
    #3072
    #2048
    def setMapGeo(self):
        x = 0
        y = 0
        with open("Assets/Level1BG.txt", mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                x = 0
                for tile in lines:
                    if tile in self.bgTileDict:
                        self.bgTiles.append((tile, x, y))
                    else:
                        pass
                    x += 512
                y += 512


        collision_size = 100
        x = 0
        y = 0
        half_start = self.tileSize/2 - collision_size/2
        half_width = self.tileSize/2 + collision_size/2

        with open("Assets/Level1FG.txt", mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                x = 0
                for tile in lines:

                    #set collision boxes
                    if tile == "2WayH":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, self.tileSize, collision_size)
                        self.collisionSet.append(rect)

                    elif tile == "2WayV":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y, collision_size, self.tileSize)
                        self.collisionSet.append(rect)

                    elif tile == "4Way":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, self.tileSize, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y, collision_size, self.tileSize)
                        self.collisionSet.append(rect)

                    elif tile == "1WayLeft":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, half_width - 30, collision_size)
                        self.collisionSet.append(rect)

                    elif tile == "1WayUp":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y, collision_size, half_width - 30)
                        self.collisionSet.append(rect)

                    elif tile == "1WayRight":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start + 30, y + half_start, half_width - 30, collision_size)
                        self.collisionSet.append(rect)

                    elif tile == "1WayDown":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y + half_start + 30, collision_size, half_width - 30)
                        self.collisionSet.append(rect)

                    elif tile == "3WayDown":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, self.tileSize, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y + half_start, collision_size, half_width)
                        self.collisionSet.append(rect)

                    elif tile == "3WayLeft":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y, collision_size, self.tileSize)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)

                    elif tile == "3WayUp":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, self.tileSize, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y, collision_size, half_width)
                        self.collisionSet.append(rect)

                    elif tile == "3WayRight":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y, collision_size, self.tileSize)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)

                    elif tile == "2WayBR":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y, collision_size, half_width)
                        self.collisionSet.append(rect)

                    elif tile == "2WayTR":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y + half_start, collision_size, half_width)
                        self.collisionSet.append(rect)

                    elif tile == "2WayTL":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y + half_start, collision_size, half_width)
                        self.collisionSet.append(rect)

                    elif tile == "2WayBL":
                        self.fgTiles.append((tile, x, y))
                        rect = pygame.Rect(x + half_start, y + half_start, half_width, collision_size)
                        self.collisionSet.append(rect)
                        rect = pygame.Rect(x + half_start, y, collision_size, half_width)
                        self.collisionSet.append(rect)

                    else:
                        pass

                    x += 512
                y += 512

        # add the tiles to the surface
        for tile in self.bgTiles:
            self.bgTileset.set_clip(pygame.Rect(self.bgTileDict[tile[0]]))
            self.image = self.bgTileset.subsurface(self.bgTileset.get_clip())
            self.rect = self.image.get_rect()
            self.rect.topleft = (tile[1], tile[2])

            self.mapSurface.blit(self.image, self.rect)

        for tile in self.fgTiles:
            self.fgTileset.set_clip(pygame.Rect(self.fgTileDict[tile[0]][0]))
            self.image = self.fgTileset.subsurface(self.fgTileset.get_clip())
            self.image = pygame.transform.rotate(self.image, self.fgTileDict[tile[0]][1])

            self.rect = self.image.get_rect()
            self.rect.topleft = (tile[1], tile[2])

            self.mapSurface.blit(self.image, self.rect)

    def draw(self, world, camera_x, camera_y):
        world.blit(self.mapSurface, (camera_x, camera_y))
