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

window = pg.display.set_mode(flags=pg.FULLSCREEN)
ww, wh = window.get_size()

# Some likely global variable
running = True

# Init background
bkgr = pg.transform.scale(pg.image.load(BKGR_PATH).convert(), (ww, wh))

# init and compile assets
player1 = player.Player(window)
info1 = infobar.Infobar(window)

lvls = [
    [chickens.Chickens(ASSET_PATH + "DroneChicken.png", window), "Chapter 1: The Initial Wave"],
    [chickens.Chickens(ASSET_PATH + "ChickenRegular.png", window, 4, 13, 2000), "Chapter 2: Straigth Jumps"],
    [chickens.Chickens(ASSET_PATH + "MilitaryChicken.png", window, 8, 13, 1850), "Chapter 3: You are wrecked!"]
]

def render_lvl(lvl=lvls[0], slide_var=True):
    lvl[0].slide_shit()
    lvl[0].slide(slide_var)
    player1.check(lvl[0], info1)
    player1.draw_bullet(lvl[0], info1)
    info1.draw(lvl[1])

def handle(slide_var=True):
    global running

    # Background handling
    window.blit(bkgr, (0, 0))

    # Render revel
    render_lvl()
    
    # Game draw
    player1.draw()

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    player1.handle_keys(pg.key.get_pressed())
    pg.display.flip()

while running:
    clk.tick(FPS)
    handle()