import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien 

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """ Respond to keydown release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullets(ai_settings,screen,ship,bullets):
    """ Fires the no of bullet assigned"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullets = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullets)

def check_keyup_events(event,ship):
    """ Respond to keyup release"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """ Respond to click events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,aliens,
                                ship,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,aliens,
                        ship,bullets,mouse_x,mouse_y):
    """ Check the click of the mouse on the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game settings
        ai_settings.initalize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        # reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # reset the game statistics
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()
        
        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,sb,stats,ship,aliens,bullets,play_button):
    """ Update the functions of screen """
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # draw the score
    sb.show_score()

    # make the play button visible
    if not stats.game_active:
        play_button.draw_button()
    # make the recently screen drawn visible
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """ Updates the no of bullets """
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_alien_bullet_collision(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_alien_bullet_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """ Respond to the alien and bullet collision"""
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if len(aliens) == 0:
        # destroy the existing bullets and add a new fleet
        bullets.empty()
        # increase the speed of the fleet
        ai_settings.increase_speed()
        # If the entire fleet is destroyed start new level
        stats.level += 1 
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height - 
                            (3* alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - (2* alien_width)
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def create_aliens(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width 
    alien.x = alien_width + 2*alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """ Making a fleet of aliens"""
    # check the space available for aliens in a row
    # assign the aliens in available space
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    number_aliens_x =  get_number_aliens_x(ai_settings,alien.rect.width )
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_aliens(ai_settings,screen,aliens,alien_number,row_number)      
def check_fleet_edges(ai_settings,aliens):
    """ Respond appropriately if the alien reached the edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    """ Drop the entire fleet and change the fleet direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """ Respond to the ship hit by alien """
    # Decrement ship limit
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # update scoreboard
        sb.prep_ship()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # create a new fleet and center the ship
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

    # pause
    sleep(0.5)
def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """ Check if any alien has reached the bottom """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this same as the ship got hit
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """ Check the alien if it is at edge,
    update the alien position"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    # look for aliens hitting on the bottom
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def check_high_score(stats,sb):
    """ Check to see if there is high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score 
        sb.prep_high_score()
