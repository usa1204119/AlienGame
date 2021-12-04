import pygame
class Settings():
    def __init__(self):
        """ Initalize the games static settings"""
        self.screen_width = 1300
        self.screen_height = 800
        self.bg_color = (230,230,230)
        # ship speed setting

        # bullet settings
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullet_allowed = 3

        # alien setting
        self.fleet_drop_speed = 25
        
        # game statistics
        self.ship_limit = 1

        # how quickly the game speeds up
        self.speedup_scale = 1.1 
        # how quickly the score increases
        self.score_scale = 1.5

        self.initalize_dynamic_settings()

        
    def initalize_dynamic_settings(self):
        """ Initalize settings that change throughout the game"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 2
        # fleet direction of 1 represents right and of -1 represents left
        self.fleet_direction = 1
        # scoring
        self.alien_points = 50 

    def increase_speed(self):
        """ Increase speed setting and scoring values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # scoring 
        self.alien_points = int(self.alien_points * self.score_scale)

