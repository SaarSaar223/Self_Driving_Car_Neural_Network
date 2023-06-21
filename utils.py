import pygame
import time
import math


def scale_image(img, scale_factor):
    size = round(int(img.get_width()) * scale_factor), round(img.get_height() * scale_factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(window, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
    window.blit(rotated_image, new_rect.topleft)
