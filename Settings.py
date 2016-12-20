class Game_Settings():

    def __init__(self):
        #Screen Settings
        self.screen_width=1200
        self.screen_height=700
        self.screen_color=(139,150,164)
        self.alien_space_y = 60
        self.alien_space_x = 60
        self.alien_center = 0
        self.score_board_height = 20


        self.fleet_drop_speed = 14
        self.bullet_limit=4
        self.ship_limit=3
        self.speedup_scale = 1.3
        self.initialize_dynamic_settings()



    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 15
        self.alien_speed_factor = 15
        self.fleet_direction = -1
        self.alien_points = 100

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *=1.1