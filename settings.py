import pygame as pg

# data properties
MINES = 40
WIDTH = 16
HEIGHT = 16

# vals
TILESIZE = 32  # this is not meant to be changed as it is dependent on the image
W = TILESIZE * WIDTH
H = TILESIZE * HEIGHT + TILESIZE
FPS = 60
LEFT = 1
RIGHT = 3

#Colour    R    G    B
colours = {1: 'blue', 2: 'darkgreen', 3: 'red', 4: 'purple', 5: ' maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}

BLACK     = (0,     0,   0)
WHITE     = (255, 255, 255)
BACK      = (220, 220, 220)
RED       = (255,   0,   0)
GREEN     = (0  , 255,   0)
BLUE      = (0  ,   0, 255)
YELLOW    = (255, 255,   0)
PURPLE    = (255,   0, 255)
AQUA      = (0  , 255, 255)
GREY      = (200, 200, 200)
BGGREY = (240, 240, 240)
FONTBLUE  = pg.Color('mediumslateblue')

# fonts
pg.font.init()
SCROLLFONT = pg.font.SysFont('helvetica', 16)
BUTTONFONT = pg.font.SysFont('helvetica', 22)

