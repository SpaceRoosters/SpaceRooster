import pygame as pg
import random

ASSET_PATH = "./assets/"
SPACES = ASSET_PATH + "spaces.png"
SHOOT_EFFECT = ASSET_PATH + "shoot.ogg"
NUT_PATH = ASSET_PATH + "neutron.png"
NUT_PACKET = ASSET_PATH + "packet.png"
EXPL_EFFECT = ASSET_PATH + "explosion.ogg"

HEIGHT = 162
DEF_SS_SPEED = 10
SHOOT_TIME = 250

class Charity:
    def __init__(self, window):
        self.window = window
        self.img = pg.image.load(SPACES).convert_alpha()
        self.x = -self.img.get_width()
        self.y = HEIGHT
        self.dead = False
        self.shoot_effect = pg.mixer.Sound(SHOOT_EFFECT)
        self.shoot_effect.set_volume(0.2)
        self.ammo = pg.image.load(NUT_PATH).convert_alpha()
        self.packet = pg.image.load(NUT_PACKET).convert_alpha()
        self.expl_effect = pg.mixer.Sound(EXPL_EFFECT)
        self.expl_effect.set_volume(0.2)
        self.shoot_timer = SHOOT_TIME
        self.last_shoot_time = 0
        self.speed = DEF_SS_SPEED
        self.shits = []

    def slide(self, **_):
        if not self.dead:
            self.x += self.speed
            self.window.blit(self.img, (self.x, self.y))

    def slide_shit(self):
        self.shit()

        for shit in self.shits:
            shit["y"] += random.randint(1, self.speed)
            self.window.blit(self.packet if shit["packet"] else self.ammo, (shit["x"], shit["y"]))
        
            if shit["y"] > self.window.get_height():
                self.shits.remove(shit)

    def shit(self):
        ticks = pg.time.get_ticks()
        if ticks - self.last_shoot_time >= self.shoot_timer:
            self.last_shoot_time = ticks
            if not self.dead and (self.x >= 0 and self.x <= self.window.get_width()):
                self.shits.append({"x": self.x + self.img.get_width() // 2, "y": self.y + self.img.get_height(), "packet": False})

    def collided_shit(self, spaceship=None):
        for shit in self.shits:
            if spaceship.colliderect(self.ammo.get_rect(x=shit["x"], y=shit["y"])):
                self.shits.remove(shit)
                return "ammo" if shit["packet"] else "egg"
        
        return ""

    def is_over(self):
        return (self.dead or self.x > self.window.get_width()) and len(self.shits) <= 0

    def collided(self, box, **_):
        if box.colliderect(self.img.get_rect(x=self.x, y=self.y)) and not self.dead:
            self.dead = True

            if random.getrandbits(1):
                self.shits.append({"x": self.x + self.img.get_width() // 2, "y": self.y + self.img.get_height(), "packet": True})
            
            self.expl_effect.play()
            return True

        return False
