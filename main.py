import pygame as pg
import chickens
import player
import scorebar

ASSET_PATH = "./assets/"
BKGR_PATH = ASSET_PATH + "bkg.jpg"
MUSIC_PATH = ASSET_PATH + "music.mp3"
FPS = 120

# init window
pg.init()
pg.display.set_caption("Space Roosters")
clk = pg.time.Clock()

# init music
pg.mixer.init()
pg.mixer.music.set_volume(1.0)
pg.mixer.music.load(MUSIC_PATH)
pg.mixer.music.play(loops=-1, fade_ms=2000)

window = pg.display.set_mode(flags=pg.FULLSCREEN)
ww, wh = pg.display.get_surface().get_size()

# Some likely global variable
running = True

# Init background
bkgr = None

def initBkgr():
    global bkgr
    bkgr = pg.transform.scale(pg.image.load(BKGR_PATH), (ww, wh))

# init and compile assets
kokoske = chickens.Chickens(ASSET_PATH + "DroneChicken.png", window)
player1 = player.Player(window)
score1 = scorebar.Scorebar(window)

initBkgr()

def handle():
    global running

    # Background handling
    window.fill("black") # clear screen
    window.blit(bkgr, (0, 0))
    
    # Game draw
    kokoske.draw()
    player1.draw()
    player1.check_life(kokoske, score1)
    score1.draw()
    player1.draw_bullet(kokoske, score1)

    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    player1.handle_keys(pg.key.get_pressed())
    pg.display.flip()

while running:
    handle()

    while not kokoske.slide():
        handle()    
    
    clk.tick(FPS)