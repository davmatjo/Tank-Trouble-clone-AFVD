import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet, Mortar, WallDestroyer, Shotgun, Laser
from Tank import Tank
from maths import degcos
from maths import degsin
from maths import arctandeg
from random import randrange, choice
from powerups import Powerup
from multiplayer import controller_movement, player_1_movement
window_size = (800, 800)
FPS = 60
fps_clock = pygame.time.Clock()
scores = [0, 0, 0]
special_bullets = []


class ai:
    def __init__(self, position):
        self.position = position
        self.player_in_range = False
        self.enemy_position = [0, 0]
        self.angle = 0
        self.fire_delay = 99

    def get_player_angle(self):
        enemy_x = self.enemy_position[0]
        enemy_y = self.enemy_position[1]
        if enemy_x > 0:
            if enemy_y > 0:
                return arctandeg(enemy_x, -enemy_y)
            if enemy_y < 0:
                return arctandeg(enemy_x, -enemy_y) + 360
        if enemy_x < 0:
            return arctandeg(enemy_x, -enemy_y) + 180
        return self.angle

    def next_move(self):
        if self.player_in_range:
            self.shoot_at_player()

    def shoot_at_player(self):
        self.angle = self.get_player_angle()
        self.fire_delay += 1
        if self.fire_delay >= 100:
            pass


    def move(self):
        pass

    def calculate(self):
        self.draw()

    def draw(self):
        pass




