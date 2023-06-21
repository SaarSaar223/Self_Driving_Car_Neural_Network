import pygame
import time
import math
import utils

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

class AbstractCar: 
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        self.x += self.vel*(-math.cos(self.angle * (math.pi/180)))
        self.y += self.vel*(math.sin(self.angle * (math.pi/180)))

    def drawCar(self, window):
        utils.blit_rotate_center(window, self.img, (self.x, self.y), self.angle)

    def slow_down(self):
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = (400, 50)