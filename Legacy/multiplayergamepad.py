import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet
from Tank import Tank
from sincos import degcos
from sincos import degsin
from sincos import arctandeg
from random import randrange

window_size = (800, 800)
FPS = 60
fps_clock = pygame.time.Clock()


# Controls are seperate so they can be shared between modes
def player_movement(afv, player):
    x_vel = player.get_axis(0)
    y_vel = player.get_axis(1)
    # deadzone allowance
    if not (-0.2 < x_vel < 0.2 and -0.2 < y_vel < 0.2):
        if x_vel > 0 and y_vel > 0:
            afv.set_angle(arctandeg(x_vel, -y_vel))
        if x_vel > 0 and y_vel < 0:
            afv.set_angle(arctandeg(x_vel, -y_vel) + 360)
        if x_vel < 0 and y_vel > 0:
            afv.set_angle(arctandeg(x_vel, -y_vel) + 180)
        if x_vel < 0 and y_vel < 0:
            afv.set_angle(arctandeg(x_vel, -y_vel) + 180)

        afv.velocity = [x_vel, y_vel]



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


def get_spawnpoints(maze_size, player_count):
    block_size = (window_size[0] / maze_size)
    possible_spawnpoints = []
    tank_positions = []
    y_pointer = -(block_size / 2)
    for i in range(maze_size):
        x_pointer = -(block_size / 2)
        y_pointer += block_size
        for j in range(maze_size):
            x_pointer += block_size
            possible_spawnpoints.append([x_pointer, y_pointer])

    print(possible_spawnpoints)
    for i in range(player_count):
        tank_coordinates = randrange(0, len(possible_spawnpoints) - 1)
        print(tank_coordinates)
        tank_coordinates = possible_spawnpoints.pop(tank_coordinates)
        print(tank_coordinates)
        tank_positions.append(tank_coordinates)
    return tank_positions


def start_2_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
        def __init__(self):
            self.game = True
            self.maze_size = 7
            self.new_maze()
            self.tanks = []
            self.create_players()
            pygame.joystick.init()
            self.p1 = pygame.joystick.Joystick(0)
            self.p2 = pygame.joystick.Joystick(1)
            self.p2.init()
            self.p1.init()

        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)

        def refresh(self):
            screen.blit(self.background, (0, 0))
            for tank in self.tanks:
                tank.move()
                tank.draw()
                tank.velocity = [0, 0]
            for bullet in self.tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not self.tanks[0].fired_bullets[0].alive:
                    self.tanks[0].fired_bullets.pop(0)
            for bullet in self.tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not self.tanks[1].fired_bullets[0].alive:
                    self.tanks[1].fired_bullets.pop(0)
            self.handle_inputs()
            player_movement(self.tanks[0], self.p1)
            player_movement(self.tanks[1], self.p2)

        def handle_inputs(self):
            """
            Input handler, allows quitting and firing - these actions can only happen once per keypress
            :return:
            """
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0:
                        if len(self.tanks[0].fired_bullets) < 10:
                            print("Fire!")
                            self.tanks[0].fired_bullets.append(Bullet(screen, [self.tanks[0].position[0], self.tanks[0].position[1]],
                                                                      [2 * degcos(self.tanks[0].angle), -2 * degsin(
                                                                     self.tanks[0].angle)]))
                    if event.button == 0 and event.joy == 1:
                        if len(self.tanks[1].fired_bullets) < 10:
                            print("Fire!")
                            self.tanks[1].fired_bullets.append(Bullet(screen, [self.tanks[1].position[0], self.tanks[1].position[1]],
                                                                      [2 * degcos(self.tanks[1].angle), -2 * degsin(
                                                                     self.tanks[1].angle)]))
                if event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        game.game = False

        def create_players(self):
            tank_positions = get_spawnpoints(self.maze_size, 2)
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))


    # initialising of all arrays and objects preparing for game
    game = MainGame()

    # main game loop
    while game.game:
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)


def start_3_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
        def __init__(self):
            self.game = True
            self.maze_size = 8
            self.new_maze()
            self.tanks = []
            self.create_players()
            self.p1 = pygame.joystick.Joystick(0)
            self.p2 = pygame.joystick.Joystick(1)
            self.p3 = pygame.joystick.Joystick(2)
            self.p1.init()
            self.p2.init()
            self.p3.init()


        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)

        def refresh(self):
            screen.blit(self.background, (0, 0))
            for tank in self.tanks:
                tank.move()
                tank.draw()
                tank.velocity = [0, 0]
            for bullet in self.tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not self.tanks[0].fired_bullets[0].alive:
                    self.tanks[0].fired_bullets.pop(0)
            for bullet in self.tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not self.tanks[1].fired_bullets[0].alive:
                    self.tanks[1].fired_bullets.pop(0)
            for bullet in self.tanks[2].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                if not self.tanks[2].fired_bullets[0].alive:
                    self.tanks[2].fired_bullets.pop(0)
            self.handle_inputs()

        def handle_inputs(self):
            """
            Input handler for all players
            :return:
            """
            player_movement(self.tanks[0], self.p1)
            player_movement(self.tanks[1], self.p2)
            player_movement(self.tanks[2], self.p3)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        if len(self.tanks[0].fired_bullets) < 10:
                            print("Fire!")
                            self.tanks[0].fired_bullets.append(Bullet(screen, [self.tanks[0].position[0], self.tanks[0].position[1]],
                                                                      [2 * degcos(self.tanks[0].angle), -2 * degsin(
                                                                     self.tanks[0].angle)]))
                    if event.key == K_KP0:
                        if len(self.tanks[1].fired_bullets) < 10:
                            print("Fire!")
                            self.tanks[1].fired_bullets.append(Bullet(screen, [self.tanks[1].position[0], self.tanks[1].position[1]],
                                                                      [2 * degcos(self.tanks[1].angle), -2 * degsin(
                                                                     self.tanks[1].angle)]))
                    if event.key == K_o:
                        if len(self.tanks[2].fired_bullets) < 10:
                            print("Fire!")
                            self.tanks[2].fired_bullets.append(Bullet(screen, [self.tanks[2].position[0], self.tanks[2].position[1]],
                                                                      [2 * degcos(self.tanks[2].angle), -2 * degsin(
                                                                     self.tanks[2].angle)]))
                    if event.key == K_ESCAPE:
                        game.game = False

        def create_players(self):
            tank_positions = get_spawnpoints(self.maze_size, 3)
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))
            self.tanks.append(Tank(screen, tank_positions[2], "Player 3", "Assets/AFV1.png"))


    game = MainGame()

    while game.game:
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)