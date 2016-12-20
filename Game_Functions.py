import sys
import pygame
from time import sleep
import Objects

def update_screen(ai_settings,screen,aliens,ship,bullets,stats,play_button,score_board):
    screen.fill(ai_settings.screen_color)

    ship.draw_ship()
    for alien in aliens.sprites():
        alien.draw_alien()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        play_button.draw_button()
    if stats.gameover:
        score_board.prep_gameover()
    score_board.draw_score()
    pygame.display.flip()

def save_highscore(stats):
    with open('Highscore', 'w') as file:
        file.write(('%d' % stats.high_score))

def check_keydown_events(events,ai_settings, screen ,ship, bullets):
    if events.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif events.key == pygame.K_LEFT:
        ship.moving_left = True
    if events.key == pygame.K_SPACE:
        load_bullets(ai_settings,screen,ship,bullets)


def check_keyup_events(events, ship):
    if events.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif events.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen ,ship, bullets,stats,play_button,aliens,sb):
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            save_highscore(stats)
            sys.exit()
        if events.type == pygame.KEYDOWN:
            check_keydown_events(events,ai_settings, screen ,ship, bullets)
        if events.type == pygame.KEYUP:
            check_keyup_events(events,ship)
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,bullets,aliens,ship,ai_settings,screen,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,bullets,aliens,ship,ai_settings,screen,sb):
    button_clicked=play_button.pos.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats(sb)
        sb.prep_ships()
        stats.game_active=True
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def load_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_limit:
        new_bullet = Objects.Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(aliens,bullets,stats,ai_settings,sb):
    bullets.update()
    for bullet in bullets:
        if bullet.pos.top <= 0:
            bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if collisions:
            stats.score+= ai_settings.alien_points
            sb.prep_score()
            if stats.score > stats.high_score:
                stats.high_score = stats.score
                sb.prep_highscore()



def get_number_rows(ai_settings, ship_height, alien_height):

    available_space_y = (ai_settings.screen_height - 2 * alien_height - ship_height)
    number_rows = int(available_space_y/ ( 1.7 * alien_height))
    return number_rows

def get_aliens_number_x(ai_settings,alien_width):

    available_space_x= ai_settings.screen_width -  2 *alien_width
    aliens_number_x= int(available_space_x/ (2* alien_width))
    return aliens_number_x

def create_alien(ai_settings,screen,aliens, alien_number, row_number):

    alien=Objects.Alien(ai_settings,screen)
    alien_width = alien.pos.width
    alien.x = (alien_width + ai_settings.alien_center)+ (alien_width + ai_settings.alien_space_x) * alien_number
    alien.pos.x = alien.x
    alien.pos.y = (alien.pos.height - ai_settings.score_board_height ) + \
                  (alien.pos.height + ai_settings.alien_space_y ) * row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen, ship, aliens):
    alien=Objects.Alien(ai_settings,screen)
    number_aliens_x=get_aliens_number_x(ai_settings,alien.pos.width)
    number_rows = get_number_rows(ai_settings, ship.pos.height, alien.pos.height)

    for rows in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number, rows)


def check_alien_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    screen_pos=screen.get_rect()
    for alien in aliens.sprites():
        if alien.pos.bottom >= screen_pos.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
            break

def chang_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.pos.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            chang_fleet_direction(ai_settings,aliens)
            break

def update_aliens(ai_settings,stats, screen,ship,aliens,bullets,sb):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)
        stats.level+=1
        sb.prep_level()

    if pygame.sprite.spritecollideany(ship,aliens) :
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)

    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets,sb)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):


    stats.ships_left -=1
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
    sleep(0.5)

    if stats.ships_left == 0:
        stats.game_active = False
        stats.gameover = True
        pygame.mouse.set_visible(True)


def update_highscore(stats):
    with open('Highscore') as file:
            score=file.read()
            stats.high_score=int(score)



