import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """ A simple attempt to model a ship"""
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # load the ship image from the directory """
        self.image = pygame.image.load('images/ship.bmp')
        # treat the image to as rectangle
        self.rect = self.image.get_rect()
        # treat the screen as rectangle
        self.screen_rect = screen.get_rect()

        # define the x axis position of the ship in center of screen
        self.rect.centerx = self.screen_rect.centerx
        # define the y position of the ship in the bottom
        self.rect.bottom = self.screen_rect.bottom
        # convert the speed into float to modify the speed as per needs
        self.center = float(self.rect.centerx)


        # define a flag set the speed to false when the key is not pressed
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.center = self.rect.centerx

    def update(self):
        """ update the speed of the ship when key is pressed"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
           self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
           self.center -= self.ai_settings.ship_speed_factor
        
        # retriving the value of speed 
        self.rect.centerx = self.center
    
    def blitme(self):
        """ Draw the contents on the screen """
        self.screen.blit(self.image,self.rect )