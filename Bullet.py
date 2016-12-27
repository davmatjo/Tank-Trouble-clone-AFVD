import pygame
from pygame.locals import *
import sys


class Bullet:
    def __init__(self, screen, position, velocity):
        """set up initial variables"""
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.image = pygame.image.load("assets/ball.png")
        self.alive = True
        self.lifetime = 0

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= -1
        if self.screen.get_at((int(self.position[0] + 6), int(self.position[1] + 3))) == (0, 0, 0, 255):
            self.velocity[0] *= -1
        if self.screen.get_at((int(self.position[0] + 3), int(self.position[1] + 6))) == (0, 0, 0, 255):
            self.velocity[1] *= -1
        if self.screen.get_at((int(self.position[0] + 3), int(self.position[1]))) == (0, 0, 0, 255):
            self.velocity[1] *= -1
        if self.screen.get_at((int(self.position[0]), int(self.position[1] + 3))) == (0, 0, 0, 255):
            self.velocity[0] *= -1

    def lifespan(self):
        self.lifetime += 1
        if self.lifetime >= 1000:
            self.alive = True

    def draw(self):
        self.screen.blit(self.image, (self.position[0], self.position[1]))