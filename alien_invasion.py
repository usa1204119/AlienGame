import pygame
from setting import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button 
from ship import Ship
import game_functions as gf 
from pygame.sprite import Group 
def run_game():
    """ run the game """
    pygame.init()
    ai_settings = Settings()
    # set the display of the required rectangle to be defined for the game
    screen = pygame.display.set_mode((1300,800))
    # set the title of the game
    pygame.display.set_caption('Alien Invasion')
    # make the play button
    play_button = Button(ai_settings,screen,"Play")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,sb,stats,ship,aliens,bullets,play_button)
run_game()
