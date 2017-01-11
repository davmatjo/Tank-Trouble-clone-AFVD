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
        # location = list(self.image_rect.center)
        # print(location[0], location[1])
        # location[0] += self.velocity[0]*2
        # print(location[0], location[1])
        # location[1] += self.velocity[1]*2
        # print(location[0], location[1])
        # self.position = (location[0], location[1])
        # print(self.image_rect.center)
        #print(self.image_rect.center)
        # print(self.image.get_rect())
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -2
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= -2
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
        # if self.screen.get_at((center[0] + 10, center[1] + 10)) == (0, 0, 0, 255):
        #     self.velocity[0] *= -1
        # if self.screen.get_at((center[0] + 10, center[1] - 10)) == (0, 0, 0, 255):
        #     self.velocity[1] *= -1
        # if self.screen.get_at((center[0] - 10, center[1] + 10)) == (0, 0, 0, 255):
        #     self.velocity[1] *= -1
        # if self.screen.get_at((center[0] - 10, center[1] - 10)) == (0, 0, 0, 255):
        #     self.velocity *= -1
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


    def turn(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle

        #loc = self.original_image.get_rect().center  # rot_image is not defined
        #print(loc)
        #self.image = pygame.transform.rotate(self.original_image, angle)
        #rot_sprite.get_rect().center = loc
        #self.image = rot_sprite


        temp_image = pygame.transform.rotate(self.original_image, self.angle)
        temp_rect = temp_image.get_rect()
        temp_rect.center = self.image_rect.center
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
        #self.image_rect = pygame.Rect.move(self.image_rect, i, -j)
        #self.pos[0] += i
        #self.pos[1] += -j



    def backward(self):
        i = degcos(self.angle)
        j = degsin(self.angle)
        self.velocity = [-i, j]
        #self.pos[0] += -i
        #self.pos[1] += j

    def draw(self):
        self.image_rect.center = (int(self.position[0]), int(self.position[1]))
        self.screen.blit(self.image, self.image_rect)

    def dead(self):
        self.original_image = self.death_image
        self.turn(0)
        self.draw()

