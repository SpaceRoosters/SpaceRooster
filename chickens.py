import pygame as pg
CHICKEN_LIVES = 2

class Chickens():
    def __init__(self, location, window):
        ww, _ = pg.display.get_surface().get_size()
        self.chickens = []
        self.speed = 10  # per pixel
        self.img = pg.image.load(location)

        for row in range(5):
            for col in range(8):
                if col % 2 == 0:
                    x = -(col * (self.img.get_width() + 10)) - self.img.get_width()
                else:
                    x = ww + (col * (self.img.get_width() + 10))

                y = (row * (self.img.get_height() + 10)) + 50
                target_x = (col * (self.img.get_width() + 10)) + (ww // 2 - self.img.get_width() * 5 + 70)
                self.chickens.append({'x': x, 'y': y, 'target': target_x, 'lives': CHICKEN_LIVES})

        self.window = window

    def slide(self):
        reached = True

        for chicken in self.chickens:
            if chicken['x'] != chicken['target']:
                if abs(chicken['x'] - chicken['target']) <= self.speed:
                    chicken['x'] = chicken['target']
                elif chicken['x'] > chicken['target']:
                    chicken['x'] -= self.speed
                    reached = False
                elif chicken['x'] < chicken['target']:
                    chicken['x'] += self.speed
                    reached = False

        return reached
    
    def collided(self, ammo):
        out = False

        for chicken in self.chickens:
            if ammo.colliderect(self.img.get_rect(x=chicken["x"], y=chicken["y"])):
                chicken["lives"] -= 1
                if chicken["lives"] <= 0:
                    self.chickens.remove(chicken)
                
                out = True
        
        return out

    def draw(self):
        for chicken in self.chickens:
            self.window.blit(self.img, (chicken['x'], chicken['y']))
