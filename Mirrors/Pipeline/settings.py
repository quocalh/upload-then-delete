from pygame.locals import *
import pygame as pg
from math import radians
WIDTH, HEIGHT = 1500, 950
FPS = 1000

FOV = radians(90)
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.OPENGL | pg.DOUBLEBUF)
clock = pg.time.Clock()

running = True

near, far = 0.05, 1000