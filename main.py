import pygame as pg
import chickens
import player
import infobar

ASSET_PATH = "./assets/"
BKGR_PATH = ASSET_PATH + "bkg.jpg"
FPS = 100

# init window
pg.init()
pg.display.set_caption("Space Roosters")
clk = pg.time.Clock()

window = pg.display.set_mode(flags=pg.FULLSCREEN)
ww, wh = window.get_size()

# Some likely global variable
running = True
slide_lr = False
slide_up = False
currLvlID = 0

lvls = [
    [chickens.Chickens(ASSET_PATH + "DroneChicken.png", window), "Chapter 1: The Initial Wave", True, False],
    [chickens.Chickens(ASSET_PATH + "ChickenRegular.png", window, 4, 13, 2000), "Chapter 2: Straigth Jumps", False, True],
    [chickens.Chickens(ASSET_PATH + "MilitaryChicken.png", window, 8, 13, 1850), "Chapter 3: You are wrecked!", True, True]
]

# Init background
bkgr = pg.transform.scale(pg.image.load(BKGR_PATH).convert(), (ww, wh))

# init and compile assets
player1 = player.Player(window)
info1 = infobar.Infobar(window)

def handle():
    global running
    
    # Game draw
    lvls[currLvlID][0].slide_shit()

    player1.draw()
    player1.check(lvls[currLvlID][0], info1)
    player1.draw_bullet(lvls[currLvlID][0], info1)

    info1.draw(lvls[currLvlID][1])

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    player1.handle_keys(pg.key.get_pressed())
    pg.display.flip()

while running:
    clk.tick(FPS)

    # Background
    window.blit(bkgr, (0, 0))

    if lvls[currLvlID][0].slide(lr=slide_lr, ud=slide_up):
        if lvls[currLvlID][2]:
            slide_lr = True
        if lvls[currLvlID][3]:
            slide_up = True

    handle()
    
    if lvls[currLvlID][0].is_over():
        slide_lr = False
        slide_up = False
        currLvlID += 1
        if currLvlID > len(lvls) - 1: break
