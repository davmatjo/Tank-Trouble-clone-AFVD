import pygame
from pygame.locals import *
import sys
from maths import degcos, degsin, get_player_grid

NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8


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
        if self.position[0] < 4 or self.position[0] > 795 or self.position[1] < 4 or self.position[1] > 795:
            self.alive = False
        else:
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
        """
        Set up initial variables
        :param screen: screen
        :param position: Start position of mortar
        :param velocity: Velocity of mortar
        :param bullets: list of bullets to put shrapnel into
        """
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (0, 0, 0), (int(position[0]), int(position[1])), 6)
        self.radius = 4
        self.alive = True
        self.lifetime = 0
        self.type = 1  # Being of type 1 means it cannot kill players
        self.shrapnel_directions = []

        # Generate a list of directions in a circle
        for i in range(0, 360, 5):
            self.shrapnel_directions.append([degcos(i) * 5, -degsin(i) * 5])
        self.bullets = bullets

    def move(self):
        """
        Bounce off wall to prevent out of bounds. No collision detection otherwise
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= -1



    def lifespan(self):
        """
        After 200 ticks of live, explode and delete
        :return:
        """
        self.lifetime += 1
        # Set radius as function of lifetime
        self.radius = -((0.02 * self.lifetime - 2) ** 2) + 10

        if self.lifetime >= 200:
            self.explode()
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (0, 0, 0), (int(self.position[0]), int(self.position[1])), int(self.radius))

    def explode(self):
        """
        Shoot shrapnel out at a high velocity based on on directions calculated
        :return:
        """
        for velocity in self.shrapnel_directions:
            # The initial position was offset to prevent accidental collisions
            self.bullets.append(Shrapnel(self.screen, [self.position[0] + velocity[0] * 3, self.position[1] + velocity[1] * 3], velocity))


class Shrapnel:
    def __init__(self, screen, position, velocity):
        """
        Set up initial variables
        :param screen: screen
        :param position:ninitial position
        :param velocity: velocity
        """
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (200, 0, 1), (int(position[0]), int(position[1])), 2)
        self.alive = True
        self.lifetime = 0
        self.type = 0

    def move(self):
        """
        Similar to Bullet.move() except it sticks to walls instead of bouncing
        If moving too fast it moves out of the map, the game will not crash.
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= 0
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= 0
        try:
            if self.screen.get_at((int(self.position[0] + 2), int(self.position[1]))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
                self.velocity[1] *= 0
            if self.screen.get_at((int(self.position[0]), int(self.position[1] + 2))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
                self.velocity[1] *= 0
            if self.screen.get_at((int(self.position[0]), int(self.position[1] - 2))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
                self.velocity[1] *= 0
            if self.screen.get_at((int(self.position[0] - 2), int(self.position[1]))) == (0, 0, 0, 255):
                self.velocity[0] *= 0
                self.velocity[1] *= 0
        except IndexError:
            pass

    def lifespan(self):
        """
        Same as bullet, just shorter lifespan
        :return:
        """
        self.lifetime += 1
        if self.lifetime >= 100:
            self.alive = False

    def draw(self):
        """Draw circle at correct position"""
        self.circle = pygame.draw.circle(self.screen, (200, 0, 1), (int(self.position[0]), int(self.position[1])), 2)


class WallDestroyer:
    def __init__(self, screen, position, velocity, maze, screen_size):
        """
        Set up initial variables
        :param screen: screen
        :param position: position
        :param velocity: velocity
        :param maze: the current maze object
        :param screen_size: the sie of the screen
        """
        self.maze = maze
        self.screen_size = screen_size
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.circle = pygame.draw.circle(screen, (0, 200, 1), (int(position[0]), int(position[1])), 2)
        self.alive = True
        self.lifetime = 0
        self.type = 2

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def move(self):
        """
        Checks for collisions with walls, bounces off outer walls to prevent map escape
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < 15 or self.position[0] > 785:
            self.velocity[0] *= -1
        if self.position[1] < 15 or self.position[1] > 785:
            self.velocity[1] *= -1

        # If the bullet collides with the wall, it detects which side of the bullet was hit and tries to work out
        # the maze "grid reference" that it is in when it collides, then removes the walls at that position
        # corresponding to the side of the bullet that was hit
        try:
            if self.screen.get_at((int(self.position[0] + 2), int(self.position[1]))) == (0, 0, 0, 255):
                pos = get_player_grid(self.position, self.maze.size, self.screen_size)
                self.maze.maze[pos[0]][pos[1]] -= EAST
                self.maze.render_maze()
                self.alive = False

            if self.screen.get_at((int(self.position[0]), int(self.position[1] + 2))) == (0, 0, 0, 255):
                pos = get_player_grid(self.position, self.maze.size, self.screen_size)
                self.maze.maze[pos[0]][pos[1]] -= SOUTH
                self.maze.render_maze()
                self.alive = False

            if self.screen.get_at((int(self.position[0]), int(self.position[1] - 2))) == (0, 0, 0, 255):
                pos = get_player_grid(self.position, self.maze.size, self.screen_size)
                self.maze.maze[pos[0]][pos[1]] -= NORTH
                self.maze.render_maze()
                self.alive = False

            if self.screen.get_at((int(self.position[0] - 2), int(self.position[1]))) == (0, 0, 0, 255):
                pos = get_player_grid(self.position, self.maze.size, self.screen_size)
                self.maze.maze[pos[0]][pos[1]] -= WEST
                self.maze.render_maze()
                self.alive = False

        except IndexError:
            pass

    def lifespan(self):
        self.lifetime += 1
        if self.lifetime >= 100:
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (200, 0, 1), (int(self.position[0]), int(self.position[1])), 2)


class Shotgun:
    def __init__(self, screen, position, velocity, bullets, angle):
        """set up initial variables"""
        self.screen = screen
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.circle = pygame.draw.circle(screen, (0, 0, 0), (int(position[0]), int(position[1])), 6)
        self.radius = 6
        self.alive = True
        self.lifetime = 0
        self.type = 1
        self.pellet_directions = []
        # Create a cone of velocities
        for i in range(int(self.angle - 30), int(self.angle + 30), 5):
            self.pellet_directions.append([degcos(i) * 5, -degsin(i) * 5])
        self.bullets = bullets

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def move(self):
        """
        Ignore walls and move
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < 0 or self.position[0] > 800:
            self.velocity[0] *= -1
        if self.position[1] < 0 or self.position[1] > 800:
            self.velocity[1] *= -1



    def lifespan(self):
        """
        Very short lifespan
        :return:
        """
        self.lifetime += 1
        if self.lifetime >= 30:
            self.explode()
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (0, 0, 0), (int(self.position[0]), int(self.position[1])), int(self.radius))

    def explode(self):
        for velocity in self.pellet_directions:
            self.bullets.append(Shrapnel(self.screen, [self.position[0] + velocity[0] * 3, self.position[1] + velocity[1] * 3], velocity))


class Laser:
    def __init__(self, screen, position, velocity, bullets, iteration=0):
        """set up initial variables"""
        self.screen = screen
        self.bullets = bullets
        self.position = position
        self.velocity = velocity
        self.iteration = iteration
        self.circle = pygame.draw.circle(screen, (0, 255, 0), (int(position[0]), int(position[1])), 4)
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
        """
        No collisions at all here
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


    def lifespan(self):
        """
        Count lifetime, create a bullet on first tick as long as bullet is not the 30th
        :return:
        """
        if self.lifetime == 1 and self.iteration <= 30:
            self.iteration += 1
            self.bullets.append(Laser(self.screen, [self.position[0] - self.velocity[0] * 2, self.position[1] - self.velocity[1] * 2], self.velocity, self.bullets, iteration=self.iteration))

        self.lifetime += 1
        if self.lifetime >= 80:
            self.alive = False

    def draw(self):
        self.circle = pygame.draw.circle(self.screen, (0, 200, 0), (int(self.position[0]), int(self.position[1])), 4)


