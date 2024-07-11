import pygame as pg
import random

CHICKEN_LIVES = 5
ASSET_PATH = "./assets/"
CHICKEN_SHIT = ASSET_PATH + "egg.png"
DEAD_EFFECT = ASSET_PATH + "dead.ogg"
EGG_EFFECT = ASSET_PATH + "egg.ogg"
SHIT_RATE = 15
SHIT_TIMER = 3200

class Chickens():
    def __init__(self, location, window):
        ww, _ = pg.display.get_surface().get_size()
        self.chickens = []
        self.chicken_shit = []
        self.speed = 10  # per pixel
        self.img = pg.image.load(location)
        self.shit_asset = pg.transform.scale(pg.image.load(CHICKEN_SHIT), (25, 40))
        self.dead_effect = pg.mixer.Sound(DEAD_EFFECT)
        self.dead_effect.set_volume(0.2)
        self.egg_effect = pg.mixer.Sound(EGG_EFFECT)
        self.last_shit_time = 0

        for row in range(5):
            for col in range(8):
                if col % 2 == 0:
                    x = -(col * (self.img.get_width() + 10)) - self.img.get_width()
                else:
                    x = ww + (col * (self.img.get_width() + 10))

                y = (row * (self.img.get_height() + 10)) + 80
                target_x = (col * (self.img.get_width() + 10)) + (ww // 2 - self.img.get_width() * 5 + 70)
                self.chickens.append({'x': x, 'y': y, 'target': target_x, 'lives': CHICKEN_LIVES})

        self.window = window

    def slide(self, lr=False):
        ww, _ = pg.display.get_surface().get_size()
        reached = True

        for chicken in self.chickens:
            self.window.blit(self.img, (chicken['x'], chicken['y']))

            if chicken['x'] != chicken['target']:
                if abs(chicken['x'] - chicken['target']) <= self.speed:
                    chicken['x'] = chicken['target']
                elif chicken['x'] > chicken['target']:
                    chicken['x'] -= random.randint(1, self.speed)
                    reached = False
                elif chicken['x'] < chicken['target']:
                    chicken['x'] += random.randint(1, self.speed)
                    reached = False
            
            if lr:
                chicken["target"] = random.randint(0, ww)

        return reached
                
    def slide_shit(self):
        _, wh = pg.display.get_surface().get_size()

        if len(self.chickens) > 0:
            self.shit()

            for shit in self.chicken_shit:
                shit["y"] += random.randint(1, self.speed)
                self.window.blit(self.shit_asset, (shit["x"], shit["y"]))
            
                if shit["y"] > wh:
                    self.chicken_shit.remove(shit)
                    self.egg_effect.play()
    
    def collided(self, ammo):
        out = False

        for chicken in self.chickens:
            if ammo.colliderect(self.img.get_rect(x=chicken["x"], y=chicken["y"])):
                chicken["lives"] -= 1
                if chicken["lives"] <= 0:
                    self.chickens.remove(chicken)
                    self.dead_effect.play()
                out = True
        
        return out
    
    def collided_egg(self, spaceship):
        out = False

        for shit in self.chicken_shit:
            if spaceship.colliderect(self.shit_asset.get_rect(x=shit["x"], y=shit["y"])):
                self.chicken_shit.remove(shit)
                out = True
        
        return out
    
    def shit(self):
        ticks = pg.time.get_ticks()
        if ticks - self.last_shit_time >= SHIT_TIMER:
            self.last_shit_time = ticks
            for _ in range(SHIT_RATE):
                chicken = random.choice(self.chickens)
                self.chicken_shit.append({"x": chicken["x"] + self.img.get_width() // 2, "y": chicken["y"] + self.img.get_height()})
