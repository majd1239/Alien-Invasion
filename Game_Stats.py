class GameStats():

    def __init__(self,ai_settings):

        self.ai_settings=ai_settings
        self.game_active = False
        self.score = 0
        self.high_score=0
        self.level = 1
        self.ships_left= self.ai_settings.ship_limit
        self.gameover=False
    def reset_stats(self,sb):
        self.ships_left= self.ai_settings.ship_limit
        self.score=0
        self.level = 1
        self.gameover = False
        sb.prep_score()
