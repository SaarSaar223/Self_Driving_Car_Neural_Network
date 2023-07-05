import pygame
import time
import math
import utils

TRACK = utils.scale_image(pygame.image.load("imgs/track.png"), 0.9)
TRACK_BORDER = utils.scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
CAR = utils.scale_image(pygame.image.load("imgs/car.png"), 0.25)
FPS = 60
BORDER_COLOR = (111,112,116)



class AbstractCar: 
    def __init__(self, max_vel, rotation_vel):
        self.img = CAR
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = 400, 50
        self.acceleration = 0.1
        self.radars = []
        self.alive = True
        self.distance = 0
        self.time = 0
        self.center = [self.x + self.img.get_width()/2, self.y + self.img.get_height()/2] 

    def rotate(self, left = False, right = False):
        if self.vel > 0:
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.distance += self.vel
        self.time += 1
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        self.x += self.vel*(-math.cos(self.angle * (math.pi/180)))
        self.y += self.vel*(math.sin(self.angle * (math.pi/180)))

    def drawCar(self, window):
        if self.collide(TRACK_BORDER_MASK) is not None:
            self.alive = False

        self.center = [self.x + self.img.get_width()/2, self.y + self.img.get_height()/2] 
        utils.blit_rotate_center(window, self.img, (self.x, self.y), self.angle)
        self.draw_radar(window)
        print(self.radars)
        self.radars = []

    def slow_down(self):
        self.vel = max(self.vel - self.acceleration, 0)
        self.move()


    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def draw_radar(self, window):
        self.make_radar()
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(window, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(window, (0, 255, 0), position, 5)

    def make_radar(self):
        for degree in range(90, 305, 45):
            length = 0
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

            while TRACK.get_at((x, y)) == BORDER_COLOR and length < 300:
                length = length + 1
                x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
                y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

            dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
            self.radars.append([(x, y), dist])

    def get_data(self):
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Basic Alive Function
        return self.alive
    
    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.distance / (CAR.get_width()/ 2)
