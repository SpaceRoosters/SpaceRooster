import pygame as pg

class Chickens():
    def __init__(self, location, window):
        self.chickens = []
        self.speed = 10  # per pixel

        ww, _ = pg.display.get_surface().get_size()
        img = pg.image.load(location)

        for row in range(5):
            for col in range(8):
                if col % 2 == 0:
                    x = -(col * (img.get_width() + 10)) - img.get_width()
                else:
                    x = ww + (col * (img.get_width() + 10))

                y = (row * (img.get_height() + 10)) + 50
                target_x = (col * (img.get_width() + 10)) + (ww // 2 - img.get_width() * 5 + 70)
                self.chickens.append({'x': x, 'y': y, 'target': target_x})

        self.window = window
        self.img = img

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

    def draw(self):
        for chicken in self.chickens:
            self.window.blit(self.img, (chicken['x'], chicken['y']))
