import pygame as pg

ASSET_PATH = "./assets/"
SS_PATH = ASSET_PATH + "ss.png"
DEF_KB = {"up": pg.K_UP, "down": pg.K_DOWN, "left": pg.K_LEFT, "right": pg.K_RIGHT, "fire": pg.K_SPACE}

class Player:
    def __init__(self, window, keys=DEF_KB):
        ww, wh = pg.display.get_surface().get_size()
        self.img = pg.transform.scale(pg.image.load(SS_PATH), (112, 100))
        self.pos = (ww // 2, wh - 162)
        self.speed = 1 # per pixel
        self.window = window
        self.handling_keys = keys
    
    def handle_keys(self, keys):
        if keys[self.keys["up"]]:
            pass

    def draw(self):
        self.window.blit(self.img, self.pos)
        