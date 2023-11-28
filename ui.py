import pygame

class UI():

    #this will extend to have a text box location as well
    def __init__(self, ui_x, ui_y, scale):

        self.scale = scale

        self.frameWidth = 251
        self.frameHeight = 301

        #load the UI
        self.torch_sheet = pygame.image.load("Assets/Torch_UI_Spritesheet.png").convert_alpha()
        self.torch_sheet.set_clip(0, 0, self.frameWidth, self.frameHeight)
        self.torch_image = self.torch_sheet.subsurface(self.torch_sheet.get_clip())
        self.torch_rect = self.torch_image.get_rect()

        #scale the UI
        self.torch_image = pygame.transform.scale(self.torch_image,(int(self.torch_rect.width*scale), \
                                                                    int(self.torch_rect.height*scale)))
        self.torch_rect = self.torch_image.get_rect()

        self.torch_rect.topleft = (ui_x, ui_y)

        self.health_frames = { 0: (0, 0, self.frameWidth,  self.frameHeight), \
                           1: (261, 0, self.frameWidth,  self.frameHeight), \
                           2: (0, 311, self.frameWidth,  self.frameHeight), \
                            }
        #flare count UI
        self.flare_x = self.torch_rect.right - 70
        self.flare_y = self.torch_rect.centery + 30
        self.flare_count = 0
        self.flare_image = pygame.image.load("Assets/Flare_UI_Sprite.png").convert_alpha()


        # Key UI
        self.key_x = self.torch_rect.right - 70
        self.key_y = self.torch_rect.centery + 70

        self.has_key = False

        self.key_image = pygame.image.load("Assets/Key_Sprite.png").convert_alpha()
        self.key_rect = self.key_image.get_rect()

        self.key_image = pygame.transform.scale(self.key_image,(int(self.key_rect.width * 0.25), \
                                                                    int(self.key_rect.height * 0.25)))



    def update(self, health, flare_count, has_key):

        if health > 0.67:
            self.torch_sheet.set_clip(pygame.Rect(self.health_frames[0]))
        elif health > 0.33:
            self.torch_sheet.set_clip(pygame.Rect(self.health_frames[1]))
        else:
            self.torch_sheet.set_clip(pygame.Rect(self.health_frames[2]))

        self.torch_image = self.torch_sheet.subsurface(self.torch_sheet.get_clip())
        self.torch_image = pygame.transform.scale(self.torch_image,(int(self.torch_rect.width), \
                                                                    int(self.torch_rect.height)))
        self.flare_count = flare_count
        self.has_key = has_key

    def draw(self, view):

        view.blit(self.torch_image, (self.torch_rect.left, self.torch_rect.top))
        for i in range(self.flare_count):
            view.blit(self.flare_image, (self.flare_x + i*20, self.flare_y))

        if self.has_key:
            view.blit(self.key_image, (self.key_x, self.key_y))
