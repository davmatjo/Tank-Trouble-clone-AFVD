import pygame
from pygame.locals import *
import sys
from sincos import degcos, degsin


class Bullet:
    def __init__(self, screen, position, velocity):
        """set up initial variables"""
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (0, 0, 0), (int(position[0]), int(position[1])), 4)
        self.alive = True
        self.lifetime = 0
        self.type = 0

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
        if self.screen.get_at((int(self.position[0] + 4), int(self.position[1]))) == (0, 0, 0, 255):
            self.velocity[0] *= -1
        if self.screen.get_at((int(self.position[0]), int(self.position[1] + 4))) == (0, 0, 0, 255):
            self.velocity[1] *= -1
        if self.screen.get_at((int(self.position[0]), int(self.position[1] - 4))) == (0, 0, 0, 255):
            self.velocity[1] *= -1
        if self.screen.get_at((int(self.position[0] - 4), int(self.position[1]))) == (0, 0, 0, 255):
            self.velocity[0] *= -1

    def lifespan(self):
        self.lifetime += 1
        if self.lifetime >= 1000:
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (0, 0, 0), (int(self.position[0]), int(self.position[1])), 4)


class Mortar:
    def __init__(self, screen, position, velocity, bullets):
        """set up initial variables"""
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (0, 0, 0), (int(position[0]), int(position[1])), 6)
        self.radius = 4
        self.alive = True
        self.lifetime = 0
        self.type = 1
        self.shrapnel_directions = []
        for i in range(0, 360, 5):
            self.shrapnel_directions.append([degcos(i) * 5, -degsin(i) * 5])
        self.bullets = bullets

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



    def lifespan(self):
        self.lifetime += 1
        self.radius = -((0.02 * self.lifetime - 2) ** 2) + 10
        if self.lifetime >= 200:
            self.explode()
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (0, 0, 0), (int(self.position[0]), int(self.position[1])), int(self.radius))

    def explode(self):
        for velocity in self.shrapnel_directions:
            self.bullets.append(Shrapnel(self.screen, [self.position[0] + velocity[0] * 4, self.position[1] + velocity[0] * 4], velocity))



class Shrapnel:
    def __init__(self, screen, position, velocity):
        """set up initial variables"""
        print(velocity)
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (200, 0, 1), (int(position[0]), int(position[1])), 2)
        self.alive = True
        self.lifetime = 0
        self.type = 0

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
            self.velocity[0] *= 0
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= 0
        try:
            if self.screen.get_at((int(self.position[0] + 2), int(self.position[1]))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
            if self.screen.get_at((int(self.position[0]), int(self.position[1] + 2))) == (0, 0, 0, 255):
                self.velocity[1] *= 0
            if self.screen.get_at((int(self.position[0]), int(self.position[1] - 2))) == (0, 0, 0, 255):
                self.velocity[1] *= 0
            if self.screen.get_at((int(self.position[0] - 2), int(self.position[1]))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
        except IndexError:
            pass

    def lifespan(self):
        self.lifetime += 1
        if self.lifetime >= 100:
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (200, 0, 1), (int(self.position[0]), int(self.position[1])), 2)

