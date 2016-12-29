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


# Controls are seperate so they can be shared between modes
def player_1_movement(afv):
    if pygame.key.get_pressed()[K_a]:
        afv.turn(2)
    if pygame.key.get_pressed()[K_s]:
        afv.backward()
    if pygame.key.get_pressed()[K_d]:
        afv.turn(-2)
    if pygame.key.get_pressed()[K_w]:
        afv.forward()


def player_2_movement(afv):
    if pygame.key.get_pressed()[K_LEFT]:
        afv.turn(2)
    if pygame.key.get_pressed()[K_DOWN]:
        afv.backward()
    if pygame.key.get_pressed()[K_RIGHT]:
        afv.turn(-2)
    if pygame.key.get_pressed()[K_UP]:
        afv.forward()


def player_3_movement(afv):
    if pygame.key.get_pressed()[K_j]:
        afv.turn(2)
    if pygame.key.get_pressed()[K_k]:
        afv.backward()
    if pygame.key.get_pressed()[K_l]:
        afv.turn(-2)
    if pygame.key.get_pressed()[K_i]:
        afv.forward()


def start_2_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
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
            for bullet in tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not tanks[0].fired_bullets[0].alive:
                    tanks[0].fired_bullets.pop(0)
            for bullet in tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not tanks[1].fired_bullets[0].alive:
                    tanks[1].fired_bullets.pop(0)

        def handle_inputs(self):
            """
            Input handler, allows quitting and firing - these actions can only happen once per keypress
            :return:
            """
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        if len(tanks[0].fired_bullets) < 10:
                            print("Fire!")
                            tanks[0].fired_bullets.append(Bullet(screen, [tanks[0].position[0], tanks[0].position[1]],
                                                     [2 * degcos(tanks[0].angle), -2 * degsin(tanks[0].angle)]))
                    if event.key == K_KP0:
                        if len(tanks[1].fired_bullets) < 10:
                            print("Fire!")
                            tanks[1].fired_bullets.append(Bullet(screen, [tanks[1].position[0], tanks[1].position[1]],
                                                     [2 * degcos(tanks[1].angle), -2 * degsin(tanks[1].angle)]))
                    if event.key == K_ESCAPE:
                        game.game = False


    # initialising of all arrays and objects preparing for game
    game = MainGame()
    game.new_maze()
    tanks = []
    tanks.append(Tank(screen, [500, 500], "Player 1", "Assets/AFV1.png"))
    tanks.append(Tank(screen, [270, 250], "Player 2", "Assets/AFV2.png"))
    # main game loop
    while game.game:
        game.handle_inputs()
        player_1_movement(tanks[0])
        player_2_movement(tanks[1])
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)




def start_3_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
        def __init__(self):
            self.game = True

        def new_maze(self):
            my_maze = Maze(8)
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
            for bullet in tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not tanks[0].fired_bullets[0].alive:
                    tanks[0].fired_bullets.pop(0)
            for bullet in tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not tanks[1].fired_bullets[0].alive:
                    tanks[1].fired_bullets.pop(0)
            for bullet in tanks[2].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not tanks[2].fired_bullets[0].alive:
                    tanks[2].fired_bullets.pop(0)

        def handle_inputs(self):
            """
            Contains additional inputs for third player
            :return:
            """
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        if len(tanks[0].fired_bullets) < 10:
                            print("Fire!")
                            tanks[0].fired_bullets.append(Bullet(screen, [tanks[0].position[0], tanks[0].position[1]],
                                                     [2 * degcos(tanks[0].angle), -2 * degsin(tanks[0].angle)]))
                    if event.key == K_KP0:
                        if len(tanks[1].fired_bullets) < 10:
                            print("Fire!")
                            tanks[1].fired_bullets.append(Bullet(screen, [tanks[1].position[0], tanks[1].position[1]],
                                                     [2 * degcos(tanks[1].angle), -2 * degsin(tanks[1].angle)]))
                    if event.key == K_o:
                        if len(tanks[2].fired_bullets) < 10:
                            print("Fire!")
                            tanks[2].fired_bullets.append(Bullet(screen, [tanks[2].position[0], tanks[2].position[1]],
                                                     [2 * degcos(tanks[2].angle), -2 * degsin(tanks[2].angle)]))
                    if event.key == K_ESCAPE:
                        game.game = False

    game = MainGame()
    game.new_maze()
    tanks = []
    tanks.append(Tank(screen, [550, 550], "Player 1", "Assets/AFV1.png"))
    tanks.append(Tank(screen, [270, 250], "Player 2", "Assets/AFV2.png"))
    tanks.append(Tank(screen, [100, 750], "Player 3", "Assets/AFV1.png"))
    while game.game:
        game.handle_inputs()
        player_1_movement(tanks[0])
        player_2_movement(tanks[1])
        player_3_movement(tanks[2])
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)
