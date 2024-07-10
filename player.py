import pygame as pg

ASSET_PATH = "./assets/"
SS_PATH = ASSET_PATH + "ss.png"
DEF_KB = {"up": pg.K_UP, "down": pg.K_DOWN, "left": pg.K_LEFT, "right": pg.K_RIGHT, "fire": pg.K_SPACE}

class Player:
    def __init__(self, window, keys=DEF_KB):
        ww, wh = pg.display.get_surface().get_size()
        self.img = pg.transform.scale(pg.image.load(SS_PATH), (112, 100))
        self.x = ww // 2
        self.y = wh - 162
        self.speed = 10  # per pixel
        self.window = window
        self.handling_keys = keys
    
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

    def draw(self):
        self.window.blit(self.img, (self.x, self.y))
