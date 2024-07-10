import pygame as pg
import chickens
import player
import scorebar

ASSET_PATH = "./assets/"
BKGR_PATH = ASSET_PATH + "bkg.jpg"
MUSIC_PATH = ASSET_PATH + "music.mp3"

# init window
pg.init()
pg.display.set_caption("Space Roosters")

# init music
pg.mixer.init()
pg.mixer.music.set_volume(1.0)
pg.mixer.music.load(MUSIC_PATH)
pg.mixer.music.play(loops=-1, fade_ms=50000)

window = pg.display.set_mode(flags=pg.FULLSCREEN)

# Init background
bkgr = None

def initBkgr():
    global bkgr
    ww, wh = pg.display.get_surface().get_size()
    bkgr = pg.transform.scale(pg.image.load(BKGR_PATH), (ww, wh))

# init and compile assets
kokoske = chickens.Chickens(ASSET_PATH + "DroneChicken.png", window)
player1 = player.Player(window)
score1 = scorebar.Scorebar(window)

initBkgr()

def handle():
    # Background handling
    window.fill("black") # clear screen
    window.blit(bkgr, (0, 0))
    player1.draw()
    kokoske.draw()
    score1.draw()
    pg.display.flip()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            pass

    while not kokoske.slide():
        handle()    
    
    handle()