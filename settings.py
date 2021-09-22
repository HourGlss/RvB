import pygame as pg
# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
MAP_WIDTH = 71
MAP_HEIGHT = 35
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = pg.Color("DARKGREY")
PLAYERCOLOR = pg.Color("BLACK")
WALLCOLOR = pg.Color("ivory")
BRUSHCOLOR = pg.Color("GREY")
LIQUIDCOLOR = pg.Color("BLUE")
GOALCOLOR = pg.Color("YELLOW")
TILESIZE = 32
PLAYER_RADIUS = 16
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
ORIGINAL_PLAYER_SPEED = 300

MELLEE_LIFETIME = 100
MELLEE_RATE = 700

BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150