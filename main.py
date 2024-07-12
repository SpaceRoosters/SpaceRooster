import pygame as pg
import chickens
import player
import infobar

ASSET_PATH = "./assets/"
BKGR_PATH = ASSET_PATH + "bkg.jpg"
FPS = 30

# init window
pg.init()
pg.display.set_caption("Space Roosters")
clk = pg.time.Clock()

window = pg.display.set_mode()
ww, wh = window.get_size()

# Some likely global variable
running = True

# Init background
bkgr = pg.transform.scale(pg.image.load(BKGR_PATH).convert(), (ww, wh))

# init and compile assets
kokoske = chickens.Chickens(ASSET_PATH + "DroneChicken.png", window)
player1 = player.Player(window)
info1 = infobar.Infobar(window)

def handle(slide_var=True):
    global running

    # Background handling
    window.blit(bkgr, (0, 0))
    
    # Game draw
    kokoske.slide_shit()
    kokoske.slide(slide_var)

    player1.draw()
    player1.check(kokoske, info1)
    player1.draw_bullet(kokoske, info1)

    info1.draw()

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    player1.handle_keys(pg.key.get_pressed())
    pg.display.flip()

while running:
    clk.tick(FPS)
    handle()

    while not kokoske.slide():
        handle(False)