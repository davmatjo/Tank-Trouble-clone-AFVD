import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet
from Tank import Tank
from sincos import degcos
from sincos import degsin

window_size = (800, 800)
FPS = 60
fps_clock = pygame.time.Clock()


def player_1_controls(afv):
    if pygame.key.get_pressed()[K_a]:
        afv.turn(2)
    if pygame.key.get_pressed()[K_s]:
        afv.backward()
    if pygame.key.get_pressed()[K_d]:
        afv.turn(-2)
    if pygame.key.get_pressed()[K_w]:
        afv.forward()

def player_2_controls(afv):
    if pygame.key.get_pressed()[K_LEFT]:
        afv.turn(2)
    if pygame.key.get_pressed()[K_DOWN]:
        afv.backward()
    if pygame.key.get_pressed()[K_RIGHT]:
        afv.turn(-2)
    if pygame.key.get_pressed()[K_UP]:
        afv.forward()

def player_3_controls():
    pass


def start_2_player(screen):
    class MainGame:
        def __init__(self):
            self.game = True

        def new_maze(self):
            my_maze = Maze(7)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)

        def refresh(self):
            screen.blit(self.background, (0, 0))
            for tank in tanks:
                tank.move()
                tank.draw()
                tank.velocity = [0, 0]
            for bullet in bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not bullets[0].alive:
                    bullets.pop(0)
    game = MainGame()
    game.new_maze()
    tanks = []
    bullets = []
    tanks.append(Tank(screen, [500, 500], "Player 1"))
    tanks.append(Tank(screen, [250, 250], "Player 2"))
    while game.game:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        player_1_controls(tanks[0])
        player_2_controls(tanks[1])
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)




def start_3_player(screen):
    game = True