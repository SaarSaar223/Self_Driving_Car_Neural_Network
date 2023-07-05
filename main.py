import pygame
import time
import math
import utils

from AbstractCar import *

TRACK = utils.scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = utils.scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
CAR = utils.scale_image(pygame.image.load("imgs/car.png"), 0.5)
FPS = 60

#######################################################################################
def draw(window, images, player_car):
    WINDOW.fill(white)
    for image, positon in images:
        window.blit(image,positon)
    
    player_car.drawCar(window)
    pygame.display.update()


def move_player(car):
    if car.is_alive:

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            car.rotate(left=True, right=False)
        if keys[pygame.K_RIGHT]:
            car.rotate(right=True, left=False)
        if keys[pygame.K_UP]:
            moved = True
            car.move_forward()
        if keys[pygame.K_DOWN]:
            if not keys[pygame.K_UP]:
                moved = True
                car.move_backward()

        if not moved:
            car.slow_down()

def move_computer(cars, nets):
    for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10 # Left
            elif choice == 1:
                car.angle -= 10 # Right
            else:
                car.speed += .5 # Speed Up

#######################################################################################




WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
white = [255, 255, 255]
WINDOW.fill(white)
pygame.display.set_caption("Car Driving Game")
run_program = True
clock = pygame.time.Clock()
images = [(TRACK, (0,0))]

car = AbstractCar(4, 4)

while run_program:
    clock.tick(FPS)
    draw(WINDOW, images, car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_program = False
            break
    move_player(car)

    if car.collide(TRACK_BORDER_MASK) is not None:
        car.is_alive = False
    


pygame.quit()
