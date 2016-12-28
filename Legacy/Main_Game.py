__author__ = 'jonesd1'
import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet
from Tank import Tank
from sincos import degcos
from sincos import degsin


pygame.init()
window_size = (800, 800)

NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8

class MainGame:
    def __init__(self):
        self.background = pygame.image.load("maze.png")

    def new_maze(self):
        my_maze = Maze(7)
        my_maze.generate_maze()
        my_maze.render_maze()
        maze_image = pygame.image.load("maze.png").convert()
        self.background = pygame.transform.scale(maze_image, window_size)

    def refresh(self):
        screen.blit(self.background, (0, 0))
        tank1.move()
        tank1.draw()
        tank1.velocity = [0, 0]
        #tank1.velocity = [0, 0]
        for bullet in bullets:
            bullet.move()
            bullet.draw()
            bullet.lifespan()
            if not bullets[0].alive:
                bullets.pop(0)



        #tank1.turn(10)





FPS = 60
fps_clock = pygame.time.Clock()


screen = pygame.display.set_mode(window_size)
screen.fill((255, 255, 255))
game = MainGame()
bullets = []
game.new_maze()
tank1 = Tank(screen, [500, 500])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                bullets.append(Bullet(screen, [tank1.position[0], tank1.position[1]], [2 * degcos(tank1.angle), -2 * degsin(tank1.angle)]))
                print(tank1.angle)
                print(degcos(tank1.angle), degsin(tank1.angle))

    if pygame.key.get_pressed()[K_a]:
        tank1.turn(2)
    if pygame.key.get_pressed()[K_s]:
        tank1.backward()
    if pygame.key.get_pressed()[K_d]:
        tank1.turn(-2)
    if pygame.key.get_pressed()[K_w]:
        tank1.forward()

    game.refresh()
    pygame.display.update()
    fps_clock.tick(FPS)