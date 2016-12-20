import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super(Alien, self).__init__()

        self.screen=screen
        self.ai_settings=ai_settings
        self.image = pygame.image.load('images/majd.bmp')
        self.pos=self.image.get_rect()
        self.screen_pos=self.screen.get_rect()
        self.pos.x=self.pos.width/2
        self.pos.y=self.pos.height
        self.rect=self.pos

    def check_edges(self):
        if self.pos.right >= self.screen_pos.right:
            return True
        elif self.pos.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.pos.x= self.x

    def draw_alien(self):
        self.screen.blit(self.image,self.pos)


class Ship(Sprite):

    def __init__(self,screen,ai_settings):
        super(Ship, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('images/ship.bmp')
        self.pos = self.image.get_rect()
        self.screen_pos = screen.get_rect()
        self.ai_settings=ai_settings

        self.pos.centerx = self.screen_pos.centerx
        self.pos.bottom = self.screen_pos.bottom

        self.movement_x=float(self.pos.centerx)

        self.moving_right = False
        self.moving_left = False

        self.rect=self.pos

    def draw_ship(self):
        self.screen.blit(self.image,self.pos)

    def update(self):

        if self.moving_right and self.pos.right < self.screen_pos.right:
            self.movement_x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.pos.left > 0:
            self.movement_x -= self.ai_settings.ship_speed_factor

        self.pos.centerx=self.movement_x

    def center_ship(self):
        self.center = self.screen_pos.centerx


class Bullet(Sprite):
    def __init__(self,ai_settings,screen,ship):

        super(Bullet,self).__init__()
        self.screen=screen
        self.image=pygame.image.load('images/bullet.bmp')

        self.pos=self.image.get_rect()
        self.pos.centerx=ship.pos.centerx
        self.pos.bottom=ship.pos.top
        self.rect=self.pos

        self.speed_factor=ai_settings.bullet_speed_factor

        self.movement_y=float(self.pos.y)

    def update(self):
        self.movement_y -= self.speed_factor
        self.pos.y=self.movement_y

    def draw_bullet(self):
        self.screen.blit(self.image, self.pos)



class Scoreboard():

    def __init__(self,ai_settings,screen,stats):

        self.screen=screen
        self.screen_pos= self.screen.get_rect()
        self.ai_settings=ai_settings
        self.stats=stats

        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,35)
        self.font1=pygame.font.SysFont(None,65)
        self.prep_score()
        self.prep_highscore()
        self.prep_level()
        self.prep_ships()
        self.prep_gameover()


    def prep_gameover(self):
        self.gameover_image=self.font1.render("GAME OVER",True,self.text_color)
        self.gameover_pos = self.gameover_image.get_rect()
        self.gameover_pos.center=self.screen_pos.center
        self.gameover_pos.y=self.gameover_pos.y - 50
        self.screen.blit(self.gameover_image, self.gameover_pos)


    def prep_ships(self):
        self.ships_=Group()
        for ships in range(self.stats.ships_left):
            ship=Ship(self.screen,self.ai_settings)
            ship.pos.x = 10 + ships*ship.pos.width
            ship.pos.y = 10
            self.ships_.add(ship)

    def prep_level(self):
        self.level_image = self.font.render("Level "+str(self.stats.level),True,self.text_color,self.ai_settings.screen_color)
        self.level_pos = self.level_image.get_rect()
        self.level_pos.right = self.screen_pos.right - 50
        self.level_pos.top = self.score_pos.bottom

    def prep_score(self):
        rounded_score=int(round(self.stats.score,-1))
        score_str="Score  "+"{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.screen_color)

        self.score_pos=self.score_image.get_rect()
        self.score_pos.right=self.screen_pos.right - 50
        self.score_pos.top = 10

    def prep_highscore(self):
        high_score=int(round(self.stats.high_score,-1))
        high_score_str = "High Score  "+"{:,}".format(high_score)

        self.hs_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.screen_color)
        self.highscore_pos = self.hs_image.get_rect()
        self.highscore_pos.centerx = self.screen_pos.centerx
        self.highscore_pos.top =  10

    def draw_score(self):
        self.screen.blit(self.score_image,self.score_pos)
        self.screen.blit(self.hs_image,self.highscore_pos)
        self.screen.blit(self.level_image,self.level_pos)
        for ships in self.ships_.sprites():
            ships.draw_ship()



import pygame.font

class Button():
    def __init__(self,ai_settings,screen,msg):

        self.screen=screen
        self.screen_pos=self.screen.get_rect()

        self.width,self.height = 200,50
        self.color=(20,150,0)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        self.pos=pygame.Rect(0,0,self.width,self.height)
        self.pos.center = self.screen_pos.center

        self.prep_msg(msg)

    def prep_msg(self,msg):

        self.msg_image=self.font.render(msg,True,self.text_color,self.color)
        self.msg_image_pos = self.msg_image.get_rect()
        self.msg_image_pos.center = self.pos.center

    def draw_button(self):
        self.screen.fill(self.color,self.pos)
        self.screen.blit(self.msg_image,self.msg_image_pos)