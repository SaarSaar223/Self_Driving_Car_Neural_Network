import pygame
import time
import math
import utils

from AbstractCar import *
from CarFunctionalities import *

TRACK = utils.scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = utils.scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_START = pygame.image.load("imgs/finish.png")
FINISH_START = pygame.transform.rotate(FINISH_START, 90)
FINISH_END = pygame.image.load("imgs/finish.png")
FINISH_END = pygame.transform.rotate(FINISH_END, 90)
FINISH_START_MASK = pygame.mask.from_surface(FINISH_START)
FINISH_END_MASK = pygame.mask.from_surface(FINISH_END)
CAR = utils.scale_image(pygame.image.load("imgs/white-car.png"), 0.12)
FPS = 60

#######################################################################################

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
white = [255, 255, 255]
WINDOW.fill(white)
pygame.display.set_caption("Car Driving Game")
run_program = True
clock = pygame.time.Clock()
images = [(TRACK, (0,0)), (FINISH_START, (500,30))]

car = PlayerCar(4, 4)

while run_program:
    clock.tick(FPS)
    draw(WINDOW, images, car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_program = False
            break
    move_player(car)

    if car.collide(TRACK_BORDER_MASK) is not None:
        car = PlayerCar(4, 4)
    
    poi =  car.collide(FINISH_START_MASK, 500, 30)
    if poi:
        if poi[0] == 0:
            car = PlayerCar(4, 4)
        else:
            print("finish")

pygame.quit()
