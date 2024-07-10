import pygame as pg

ASSET_PATH = "./assets/"
SF_PATH = ASSET_PATH + "scorebar.ttf"
SB_PATH = ASSET_PATH + "scorebar.png"

class Scorebar:
    def __init__(self, window):
        self.lives = 3
        self.score = 0
        self.window = window
        self.font = pg.font.Font(SF_PATH, 59)
        self.img = pg.image.load(SB_PATH)
    
    def addScore(self, rScore):
        self.score += rScore
    
    def killMe(self):
        self.lives -= 1

    def draw(self):
        self.window.blit(self.img, (0, 0))
        self.window.blit(self.font.render("{:,}".format(self.score), True, "white"), (15, 0))
        self.lives += self.score // 1000000
        self.window.blit(self.font.render(str(self.lives), True, "white"), (400, 0))