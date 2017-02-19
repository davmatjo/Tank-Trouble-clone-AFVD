import pygame
from pygame.locals import *
import sys
from Bullet import Bullet
from maths import degcos
from maths import degsin


class Tank:
    def __init__(self, screen, position, name, sprite):
        """set up initial variables"""
        self.screen = screen
        self.velocity = [0, 0]
        self.original_image = pygame.image.load(sprite)
        self.image = self.original_image
        self.death_image = pygame.image.load("Assets/dead.png")
        self.dead_count = 0
        self.angle = 0
        # Obtain the rect of the original image
        self.image_rect = self.image.get_rect()
        self.position = position
        self.name = name
        self.powerups = 0
        self.fired_bullets = []
        self.alive = True


    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def move(self):
        center = list(self.image_rect.center)
        if self.screen.get_at((center[0] + 10, center[1])) == (0, 0, 0, 255):
            if self.velocity[0] > 0:
                self.velocity[0] = 0
        if self.screen.get_at((center[0], center[1] + 10)) == (0, 0, 0, 255):
            if self.velocity[1] > 0:
                self.velocity[1] = 0
        if self.screen.get_at((center[0] - 10, center[1])) == (0, 0, 0, 255):
             if self.velocity[0] < 0:
                 self.velocity[0] = 0
        if self.screen.get_at((center[0], center[1] - 10)) == (0, 0, 0, 255):
            if self.velocity[1] < 0:
                self.velocity[1] = 0
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


    def turn(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle

        # Store a temporary rotated image at the correct angle
        temp_image = pygame.transform.rotate(self.original_image, self.angle)
        # Obtain the bounding rect of the temporary image
        temp_rect = temp_image.get_rect()
        # Set the center of the rect
        temp_rect.center = self.image_rect.center
        # Set the temporary rect and image to the actual rect and image
        self.image = temp_image
        self.image_rect = temp_rect

    def set_angle(self, angle):
        self.angle = angle

        temp_image = pygame.transform.rotate(self.original_image, self.angle)
        temp_rect = temp_image.get_rect()
        temp_rect.center = self.image_rect.center
        self.image = temp_image
        self.image_rect = temp_rect

    def forward(self):
        i = degcos(self.angle)
        j = degsin(self.angle)
        self.velocity = [i, -j]

    def backward(self):
        i = degcos(self.angle)
        j = degsin(self.angle)
        self.velocity = [-i, j]

    def draw(self):
        """Draw tank to screen and set rect center for rotation function"""
        self.image_rect.center = (int(self.position[0]), int(self.position[1]))
        self.screen.blit(self.image, self.image_rect)

    def dead(self):
        self.original_image = self.death_image
        self.turn(0)
        self.draw()

