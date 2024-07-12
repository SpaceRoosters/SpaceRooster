import pygame as pg
import sys

ASSET_PATH = "./assets/"
SS_PATH = ASSET_PATH + "ss.png"
NUT_PATH = ASSET_PATH + "neutron.png"
SHOOT_EFFECT = ASSET_PATH + "shoot.ogg"
EXPL_EFFECT = ASSET_PATH + "explosion.ogg"
AMMO_EFFECT = ASSET_PATH + "ammo.ogg"
SHOOT_TIME = 250
CHICKEN_KILL = 150 # score
DEF_KB = {"up": pg.K_UP, "down": pg.K_DOWN, "left": pg.K_LEFT, "right": pg.K_RIGHT, "fire": pg.K_SPACE}

class Player:
    def __init__(self, window, keys=DEF_KB):
        self.window = window
        ww, wh = self.window.get_size()
        self.img = pg.transform.scale(pg.image.load(SS_PATH).convert_alpha(), (112, 100))
        self.ammo_files = {"neutron": pg.image.load(NUT_PATH).convert_alpha()}
        self.x = ww // 2
        self.y = wh - 162
        self.speed = 10  # per pixel
        self.bullet_speed = 15
        self.handling_keys = keys
        self.bullets = []
        self.last_shoot_time = 0
        self.shoot_effect = pg.mixer.Sound(SHOOT_EFFECT)
        self.shoot_effect.set_volume(0.2)   
        self.expl_effect = pg.mixer.Sound(EXPL_EFFECT)
        self.expl_effect.set_volume(0.2)
        self.shoot_boom = 1
        self.ammo_effect = pg.mixer.Sound(AMMO_EFFECT)
        self.ammo_effect.set_volume(0.6)

    def move(self, rx, ry):
        ww, wh = self.window.get_size()
        self.x += rx
        self.y += ry

        if self.y < 81:
            self.y = 81
        elif self.y > wh - 162:
            self.y = wh - 162

        if self.x < 0:
            self.x = 0
        elif self.x > ww - self.img.get_width():
            self.x = ww - self.img.get_width()

    def handle_keys(self, key):
        if key[self.handling_keys["left"]]:
            self.move(-self.speed, 0)
        if key[self.handling_keys["right"]]:
            self.move(self.speed, 0)
        if key[self.handling_keys["up"]]:
            self.move(0, -self.speed)
        if key[self.handling_keys["down"]]:
            self.move(0, self.speed)
        if key[self.handling_keys["fire"]]:
            self.shoot()
    
    def shoot(self):
        ticks = pg.time.get_ticks()
        if ticks - self.last_shoot_time >= SHOOT_TIME:
            self.last_shoot_time = ticks
            xPos = self.x + self.ammo_files["neutron"].get_width() // 2
            yPos = self.y + -self.img.get_height()
            self.bullets.append([xPos, yPos])
            self.shoot_effect.play()
    
    def check(self, chickens, scorebar):
        spaceship = self.img.get_rect(x=self.x, y=self.y)
        collide_msg = chickens.collided_shit(spaceship)
        if chickens.collided(spaceship) or collide_msg == "egg":
            self.expl_effect.play()
            scorebar.add_score(-1000)
            
            if self.shoot_boom - 1 > 0:
                self.shoot_boom -= 1
            
            if scorebar.kill_me() <= 0:
                sys.exit(-1)
        elif collide_msg == "ammo":
            self.shoot_boom += 1
            self.ammo_effect.play()
            scorebar.add_score(500)
    
    def draw_bullet(self, chickens, scorebar):
        for coor in self.bullets:
            coor[1] -= self.bullet_speed
            self.window.blit(self.ammo_files["neutron"], (coor[0], coor[1]))

            # Ammo rect
            ammo_rect = self.ammo_files["neutron"].get_rect(x=coor[0], y=coor[1])
         
            if coor[1] < 0:
                self.bullets.remove(coor)
            elif chickens.collided(ammo_rect, self.shoot_boom):
                self.bullets.remove(coor)
                scorebar.add_score(CHICKEN_KILL)

    def draw(self):
        self.window.blit(self.img, (self.x, self.y))
