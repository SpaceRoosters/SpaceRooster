import pygame as pg
import sys

ASSET_PATH = "./assets/"
SS_PATH = ASSET_PATH + "ss.png"
NUT_PATH = ASSET_PATH + "neutron.png"
SHOOT_TIME = 250
CHICKEN_KILL = 150 # score
DEF_KB = {"up": pg.K_UP, "down": pg.K_DOWN, "left": pg.K_LEFT, "right": pg.K_RIGHT, "fire": pg.K_SPACE}

class Player:
    def __init__(self, window, keys=DEF_KB):
        ww, wh = pg.display.get_surface().get_size()
        self.img = pg.transform.scale(pg.image.load(SS_PATH), (112, 100))
        self.ammo_files = {"neutron": pg.image.load(NUT_PATH)}
        self.x = ww // 2
        self.y = wh - 162
        self.speed = 10  # per pixel
        self.bullet_speed = 15
        self.window = window
        self.handling_keys = keys
        self.bullets = []
        self.last_shoot_time = 0

    def move(self, rx, ry):
        ww, wh = pg.display.get_surface().get_size()
        self.x += rx
        self.y += ry

        if self.y < 0:
            self.y = 0
        elif self.y > wh - self.img.get_height():
            self.y = wh - self.img.get_height()

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
            xPos = self.x + -self.ammo_files["neutron"].get_width() // 3
            yPos = self.y + -self.img.get_height()
            self.bullets.append([xPos, yPos])
    
    def check_life(self, chickens, scorebar):
        spaceship = self.img.get_rect(x=self.x, y=self.y)
        if chickens.collided(spaceship):
            if scorebar.kill_me() <= 0:
                sys.exit(-1)
    
    def draw_bullet(self, chickens, scorebar):
        for coor in self.bullets:
            coor[1] -= self.bullet_speed
            self.window.blit(self.ammo_files["neutron"], (coor[0], coor[1]))

            # Ammo rect
            ammo_rect = self.ammo_files["neutron"].get_rect(x=coor[0], y=coor[1])
         
            if coor[1] < 0:
                self.bullets.remove(coor)
            elif chickens.collided(ammo_rect):
                self.bullets.remove(coor)
                scorebar.add_score(CHICKEN_KILL)

    def draw(self):
        self.window.blit(self.img, (self.x, self.y))

