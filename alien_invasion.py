import pygame
import Objects
from pygame.sprite import Group
from Settings import Game_Settings
import Game_Functions as function
from Game_Stats import GameStats

def run_game():

    pygame.init()
    ai_settings= Game_Settings()

    screen=pygame.display.set_mode( (ai_settings.screen_width,ai_settings.screen_height) )
    pygame.display.set_caption("Alien Invasion")

    player_ship = Objects.Ship(screen, ai_settings)
    bullets=Group()
    aliens=Group()
    play_button =  Objects.Button(ai_settings,screen,"Play")
    function.create_fleet(ai_settings,screen,player_ship,aliens)
    stats= GameStats(ai_settings)
    function.update_highscore(stats)
    score_board = Objects.Scoreboard(ai_settings, screen, stats)


    while True:

        function.check_events(ai_settings,screen,player_ship,bullets,stats,play_button,aliens,score_board)

        if stats.game_active:
            player_ship.update()
            function.update_bullets(aliens,bullets,stats,ai_settings,score_board)
            function.update_aliens(ai_settings,stats,screen,player_ship,aliens,bullets,score_board)

        function.update_screen(ai_settings,screen,aliens,player_ship,bullets,stats,play_button,score_board)


run_game()