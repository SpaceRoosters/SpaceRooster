import pygame as pg
import random

ASSET_PATH = "./assets/"
HEN = ASSET_PATH + "MotherHen.png"
HEN_DONE = ASSET_PATH + "hen_done.png"
POP_EFFECT = ASSET_PATH + "pop.ogg"

SPEED_PART = 1.3
DEF_HEN_LIVES = 50

class Boss:
    def __init__(self, window):
        self.window = window
        self.img = pg.image.load(HEN).convert_alpha()
        self.done_img = pg.image.load(HEN_DONE).convert_alpha()
        self.x = -self.img.get_width()
        self.y = -self.img.get_height()
        self.target_x = self.window.get_width() // 2 - self.img.get_width()
        self.target_y = self.window.get_height() // 2 - self.img.get_height()
        self.lives = DEF_HEN_LIVES
        self.expl_effect = pg.mixer.Sound(POP_EFFECT)
        self.speed_part = SPEED_PART
        self.sliding = False
        self.shits = []
    
    def slide(self, spaceship, **_):
        reached = True
        self.window.blit(self.img, (self.x, self.y))

        if self.x != self.target_x:
            if abs(self.x - self.target_x) <= spaceship.speed // self.speed_part:
                self.x = self.target_x
            elif self.x > self.target_x:
                self.x -= random.randint(1, spaceship.speed // self.speed_part)
                reached = False
            elif self.x < self.target_x:
                self.x += random.randint(1, spaceship.speed // self.speed_part)
                reached = False

        if self.y != self.target_y:
            if abs(self.y - self.target_y) <= spaceship.speed // self.speed_part:
                self.y = self.target_y
            elif self.y > self.target_y:
                self.y -= random.randint(1, spaceship.speed // self.speed_part)
                reached = False
            elif self.y < self.target_y:
                self.y += random.randint(1, spaceship.speed // self.speed_part)
                reached = False

        if self.target_x == self.x and not self.sliding:
            self.target_x = spaceship.x

        if self.target_y == self.y and not self.sliding:
            self.target_y = spaceship.y
        
        if self.sliding:
            self.sliding = not reached

        return reached

    def slide_shit(self):
        pass

    def collided_shit(self, **_):
        pass

    def is_over(self):
        return self.lives <= 0 and not self.sliding

    def collided(self, box, kill_rate=1):
        if box.colliderect(self.img.get_rect(x=self.x, y=self.y)) and self.lives >= 0 and not self.sliding:
            self.lives -= kill_rate
            
            if self.lives <= 0: 
                self.img = self.done_img
                self.sliding = True
                self.target_y = self.window.get_height()
            
            self.expl_effect.play()
            return True

        return False
