import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet, Mortar, WallDestroyer, Shotgun, Laser
from Tank import Tank
from maths import degcos
from maths import degsin
from maths import arctandeg
from maths import get_player_grid
from random import randrange, choice
from powerups import Powerup

NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8


window_size = (800, 800)
FPS = 60
fps_clock = pygame.time.Clock()
scores = [0, 0, 0]
special_bullets = []


def controller_movement(afv, player):
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



# Controls are seperate so they can be shared between modes
def player_1_movement(afv, game):
    if afv.alive:
        if pygame.key.get_pressed()[K_a]:
            afv.turn(2)
        if pygame.key.get_pressed()[K_s]:
            afv.backward()
        if pygame.key.get_pressed()[K_d]:
            afv.turn(-2)
        if pygame.key.get_pressed()[K_w]:
            afv.forward()
    try:
        controller_movement(afv, game.p1)
    except:
        pass


def player_2_movement(afv, game):
    if afv.alive:
        if pygame.key.get_pressed()[K_LEFT]:
            afv.turn(2)
        if pygame.key.get_pressed()[K_DOWN]:
            afv.backward()
        if pygame.key.get_pressed()[K_RIGHT]:
            afv.turn(-2)
        if pygame.key.get_pressed()[K_UP]:
            afv.forward()
    try:
        controller_movement(afv, game.p2)
    except:
        pass


def player_3_movement(afv, game):
    if afv.alive:
        if pygame.key.get_pressed()[K_j]:
            afv.turn(2)
        if pygame.key.get_pressed()[K_k]:
            afv.backward()
        if pygame.key.get_pressed()[K_l]:
            afv.turn(-2)
        if pygame.key.get_pressed()[K_i]:
            afv.forward()
    try:
        controller_movement(afv, game.p3)
    except:
        pass


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

    for i in range(player_count):
        tank_coordinates = randrange(0, len(possible_spawnpoints) - 1)
        tank_coordinates = possible_spawnpoints.pop(tank_coordinates)
        tank_positions.append(tank_coordinates)
    return tank_positions


def bullet_decay_and_collision_handler(t_id, bullet, tank):
    if not tank[t_id].fired_bullets[0].alive:
        tank[t_id].fired_bullets.pop(0)
    if bullet.lifetime > 10:
        for u_id in range(len(tank)):
            if tank[u_id].image_rect.colliderect(bullet.circle) and bullet.type == 0:
                bullet.alive = False
                tank[u_id].alive = False


def powerup_collision_handler(tank, powerups):
    for u_id in range(len(tank)):
        for powerup in powerups:
            if tank[u_id].image_rect.colliderect(powerup.image_rect):
                powerup.alive = False
                tank[u_id].powerups = powerup.type


def shrapnel_handler(bullet, tank, game):
    if not bullet.alive:
        if bullet.type == 1:
            game.background = pygame.transform.scale(pygame.image.load("maze.png"), window_size)
        special_bullets.pop(0)
    for u_id in range(len(tank)):
        if tank[u_id].image_rect.colliderect(bullet.circle) and bullet.type == 0:
            bullet.alive = False
            tank[u_id].alive = False





def fire(t_id, tanks, screen, maze):
    if len(tanks[t_id].fired_bullets) < 10 and tanks[t_id].alive:
        if tanks[t_id].powerups == 1:
            b_velocity = [degcos(tanks[t_id].angle), -degsin(tanks[t_id].angle)]
            tanks[t_id].fired_bullets.append(Mortar(screen, [tanks[t_id].position[0] + b_velocity[0] * 18,
                                                             tanks[t_id].position[1] + b_velocity[1] * 18],
                                                    b_velocity, special_bullets))

            tanks[t_id].powerups = 0

        elif tanks[t_id].powerups == 2:
            b_velocity = [degcos(tanks[t_id].angle) * 2, -degsin(tanks[t_id].angle) * 2]
            special_bullets.append(WallDestroyer(screen, [tanks[t_id].position[0] + b_velocity[0] * 20,
                                                             tanks[t_id].position[1] + b_velocity[1] * 20],
                                                    b_velocity, maze, window_size))
            tanks[t_id].powerups = 0

        elif tanks[t_id].powerups == 3:
            b_velocity = [degcos(tanks[t_id].angle), -degsin(tanks[t_id].angle)]
            tanks[t_id].fired_bullets.append(Shotgun(screen, [tanks[t_id].position[0] + b_velocity[0] * 18,
                                                             tanks[t_id].position[1] + b_velocity[1] * 18],
                                                    b_velocity, special_bullets, tanks[t_id].angle))
            tanks[t_id].powerups = 0

        elif tanks[t_id].powerups == 4:
            b_velocity = [degcos(tanks[t_id].angle) * 15, -degsin(tanks[t_id].angle) * 15]
            tanks[t_id].fired_bullets.append(Laser(screen, [tanks[t_id].position[0] + b_velocity[0],
                                                             tanks[t_id].position[1] + b_velocity[1]],
                                                    b_velocity, tanks[t_id].fired_bullets))
            tanks[t_id].powerups = 0

        else:
            b_velocity = [2 * degcos(tanks[t_id].angle), -2 * degsin(tanks[t_id].angle)]
            tanks[t_id].fired_bullets.append(Bullet(screen, [tanks[t_id].position[0] + b_velocity[0] * 18,
                                                                  tanks[t_id].position[1] + b_velocity[1] * 18],
                                                         b_velocity))


def start_2_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
        def __init__(self):
            self.game = True
            self.maze_size = 7
            self.maze = self.new_maze()
            self.tanks = []
            self.powerups = []
            self.create_players()
            self.end_timer = 0
            pygame.joystick.init()
            try:
                self.p1 = pygame.joystick.Joystick(0)
                self.p1.init()
            except:
                pass
            try:
                self.p2 = pygame.joystick.Joystick(1)
                self.p2.init()
            except:
                pass


        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)
            return my_maze

        def refresh(self):
            screen.blit(self.background, (0, 0))
            self.powerup_handler()
            for tank in self.tanks:
                if tank.alive:
                    tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]
            for bullet in self.tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(0, bullet, self.tanks)
            for bullet in self.tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(1, bullet, self.tanks)
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                shrapnel_handler(bullet, self.tanks, game)
            powerup_collision_handler(self.tanks, self.powerups)
            self.handle_inputs()
            player_1_movement(self.tanks[0], game)
            player_2_movement(self.tanks[1], game)
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler, allows quitting and firing - these actions can only happen once per keypress
            :return:
            """
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_e and self.tanks[0].alive:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_KP0 and self.tanks[1].alive:
                        fire(1, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.game = False

                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0 and self.tanks[0].alive:
                        fire(0, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 1 and self.tanks[1].alive:
                        fire(1, self.tanks, screen, self.maze)


        def game_end_check(self):
            if not (self.tanks[0].alive and self.tanks[1].alive):
                self.end_timer += 1
                if self.end_timer >= 350:
                    if not self.tanks[0].alive and not self.tanks[1].alive:
                        self.game = False
                        start_2_player(screen)
                    elif not self.tanks[1].alive:
                        self.update_score(0)
                        self.game = False
                        start_2_player(screen)
                    elif not self.tanks[0].alive:
                        self.update_score(1)
                        self.game = False
                        start_2_player(screen)

        def update_score(self, winner):
            scores[winner] += 1
            pygame.display.set_caption("Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]))



        def create_players(self):
            tank_positions = get_spawnpoints(self.maze_size, 2)
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))


        def powerup_handler(self):
            if randrange(0, 1000) >= 998:
                points = get_spawnpoints(self.maze_size, 2)
                chosen_point = choice(points)
                if not any(item.position == chosen_point for item in self.powerups):
                    self.powerups.append(Powerup(screen, chosen_point))
            for powerup in self.powerups:
                powerup.draw()
                if not powerup.alive:
                    self.powerups.pop(self.powerups.index(powerup))

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
            self.maze = self.new_maze()
            self.tanks = []
            self.create_players()
            self.end_timer = 0
            self.powerups = []
            try:
                self.p1 = pygame.joystick.Joystick(0)
                self.p1.init()
            except:
                pass
            try:
                self.p2 = pygame.joystick.Joystick(1)
                self.p2.init()
            except:
                pass
            try:
                self.p3 = pygame.joystick.Joystick(2)
                self.p3.init()
            except:
                pass

        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)
            return my_maze

        def refresh(self):
            screen.blit(self.background, (0, 0))
            for tank in self.tanks:
                if tank.alive:
                    tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]
            for bullet in self.tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(0, bullet, self.tanks)
            for bullet in self.tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(1, bullet, self.tanks)
            for bullet in self.tanks[2].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(2, bullet, self.tanks)
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                shrapnel_handler(bullet, self.tanks, game)
            self.powerup_handler()
            powerup_collision_handler(self.tanks, self.powerups)
            self.handle_inputs()
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler for all players
            :return:
            """
            player_1_movement(self.tanks[0], game)
            player_2_movement(self.tanks[1], game)
            player_3_movement(self.tanks[2], game)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_KP0:
                        fire(1, self.tanks, screen, self.maze)
                    if event.key == K_o:
                        fire(2, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.game = False

                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0:
                        fire(0, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 1:
                        fire(1, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 2:
                        fire(2, self.tanks, screen, self.maze)

        def create_players(self):
            tank_positions = get_spawnpoints(self.maze_size, 3)
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))
            self.tanks.append(Tank(screen, tank_positions[2], "Player 3", "Assets/AFV3.png"))

        def game_end_check(self):
            if self.tanks[0].alive + self.tanks[1].alive + self.tanks[2].alive <= 1:
                self.end_timer += 1
                if self.end_timer >= 300:
                    if not self.tanks[0].alive and not self.tanks[1].alive and not self.tanks[2].alive:
                        self.game = False
                        start_3_player(screen)
                    elif not self.tanks[1].alive and not self.tanks[2].alive:
                        self.update_score(0)
                        self.game = False
                        start_3_player(screen)
                    elif not self.tanks[0].alive and not self.tanks[2].alive:
                        self.update_score(1)
                        self.game = False
                        start_3_player(screen)
                    elif not self.tanks[0].alive and not self.tanks[1]. alive:
                        self.update_score(2)
                        self.game = False
                        start_3_player(screen)

        def update_score(self, winner):
            scores[winner] += 1
            pygame.display.set_caption("Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]) + "                   Player3: " + str(scores[2]))

        def powerup_handler(self):
            if len(self.powerups) < 12:
                if randrange(0, 1000) >= 998:
                    points = get_spawnpoints(self.maze_size, 2)
                    chosen_point = choice(points)
                    if not any(item.position == chosen_point for item in self.powerups):
                        self.powerups.append(Powerup(screen, chosen_point))
                for powerup in self.powerups:
                    powerup.draw()
                    if not powerup.alive:
                        self.powerups.pop(self.powerups.index(powerup))


    game = MainGame()

    while game.game:
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)


def start_1_player(screen):
    class MainGame:
        """Class that handles some aspects of running the game, such as performing the regular calculations needed for
                every refresh"""
        def __init__(self):
            self.running = True
            self.maze_size = 7
            self.maze = self.new_maze()
            self.tanks = []
            self.powerups = []
            self.create_players()
            self.end_timer = 0
            pygame.joystick.init()
            try:
                self.p1 = pygame.joystick.Joystick(0)
                self.p1.init()
            except:
                pass

        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)
            return my_maze

        def refresh(self):
            screen.blit(self.background, (0, 0))
            self.powerup_handler()
            for tank in self.tanks:
                if tank.alive:
                    if tank == self.tanks[0]:
                        tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]
            for bullet in self.tanks[0].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(0, bullet, self.tanks)
            for bullet in self.tanks[1].fired_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                bullet_decay_and_collision_handler(1, bullet, self.tanks)
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                shrapnel_handler(bullet, self.tanks, game)
            powerup_collision_handler(self.tanks, self.powerups)
            self.handle_inputs()
            player_1_movement(self.tanks[0], game)
            ai.calculate()
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler, allows quitting and firing - these actions can only happen once per keypress
            :return:
            """
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_e and self.tanks[0].alive:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_KP0 and self.tanks[1].alive:
                        fire(1, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.running = False

                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0 and self.tanks[0].alive:
                        fire(0, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 1 and self.tanks[1].alive:
                        fire(1, self.tanks, screen, self.maze)


        def game_end_check(self):
            if not (self.tanks[0].alive and self.tanks[1].alive):
                self.end_timer += 1
                if self.end_timer >= 350:
                    if not self.tanks[0].alive and not self.tanks[1].alive:
                        self.running = False
                        start_1_player(screen)
                    elif not self.tanks[1].alive:
                        self.update_score(0)
                        self.running = False
                        start_1_player(screen)
                    elif not self.tanks[0].alive:
                        self.update_score(1)
                        self.running = False
                        start_1_player(screen)

        def update_score(self, winner):
            scores[winner] += 1
            pygame.display.set_caption("Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]))



        def create_players(self):
            self.tank_positions = get_spawnpoints(self.maze_size, 2)
            self.tanks.append(Tank(screen, self.tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, self.tank_positions[1], "Player 2", "Assets/AFV1.png"))


        def powerup_handler(self):
            if randrange(0, 1000) >= 998:
                points = get_spawnpoints(self.maze_size, 2)
                chosen_point = choice(points)
                if not any(item.position == chosen_point for item in self.powerups):
                    self.powerups.append(Powerup(screen, chosen_point))
            for powerup in self.powerups:
                powerup.draw()
                if not powerup.alive:
                    self.powerups.pop(self.powerups.index(powerup))





    # initialising of all arrays and objects preparing for game
    game = MainGame()
    ai = Ai(game.tank_positions[1], game, game.tanks, screen)

    # main game loop
    while game.running:
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)


class Ai:
    def __init__(self, position, game, tanks, screen):
        self.game = game
        self.current_movement = None
        self.tanks = tanks
        self.player_in_range = False
        self.fire_delay = 99
        self.delay = 0
        self.screen = screen
        self.previous_grid = []
        self.previous_movement = 0

    def get_player_angle(self):
        enemy_position = self.tanks[0].position
        my_position = self.tanks[1].position
        enemy_x = enemy_position[0]
        enemy_y = enemy_position[1]
        my_x = my_position[0]
        my_y = my_position[1]
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y
        if x_diff > 0:
            if y_diff > 0:
                return arctandeg(x_diff, -y_diff)
            if y_diff < 0:
                return arctandeg(x_diff, -y_diff) + 360
        if x_diff < 0:
            return arctandeg(x_diff, -y_diff) + 180
        return self.tanks[1].angle


    def shoot_at_player(self):
        self.tanks[1].set_angle(self.get_player_angle())
        print(self.tanks[1].angle)
        self.fire_delay += 1
        if self.fire_delay >= 10:
            fire(1, self.tanks, self.screen, self.game.maze.maze)
            self.fire_delay = 0

    def move(self):
        self.fire_delay = 10000
        current_grid = get_player_grid(self.tanks[1].position, self.game.maze_size, window_size)
        if self.current_movement is None:
            available_moves = []
            walls_up = self.game.maze.maze[current_grid[0]][current_grid[1]]
            print("walls:", walls_up)
            if not walls_up & NORTH and not self.previous_movement == NORTH:
                available_moves.append(NORTH)
            if not walls_up & SOUTH and not self.previous_movement == SOUTH:
                available_moves.append(SOUTH)
            if not walls_up & EAST and not self.previous_movement == EAST:
                available_moves.append(EAST)
            if not walls_up & WEST and not self.previous_movement == WEST:
                available_moves.append(WEST)
            print("moves:", available_moves)
            if not available_moves:
                available_moves.append(self.previous_movement)
            self.current_movement = choice(available_moves)

            print("moving", self.current_movement)

            self.previous_grid = current_grid
        if self.current_movement == NORTH:
            if not current_grid == self.previous_grid:
                self.stop_moving()
            self.tanks[1].position[1] -= 2
            self.tanks[1].set_angle(90)
        if self.current_movement == SOUTH:
            if not current_grid == self.previous_grid:
                self.stop_moving()
            self.tanks[1].position[1] += 2
            self.tanks[1].set_angle(270)
        if self.current_movement == EAST:
            if not current_grid == self.previous_grid:
                self.stop_moving()
            self.tanks[1].position[0] += 2
            self.tanks[1].set_angle(0)
        if self.current_movement == WEST:
            if not current_grid == self.previous_grid:
                self.stop_moving()
            self.tanks[1].position[0] -= 2
            self.tanks[1].set_angle(180)

    def stop_moving(self):
        self.delay += 1
        if self.delay >= 25:
            if self.current_movement == NORTH:
                self.previous_movement = SOUTH
            if self.current_movement == EAST:
                self.previous_movement = WEST
            if self.current_movement == SOUTH:
                self.previous_movement = NORTH
            if self.current_movement == WEST:
                self.previous_movement = EAST

            self.current_movement = None
            self.delay = 0

    def calculate(self):
        enemy_position = self.tanks[0].position
        my_position = self.tanks[1].position
        enemy_distance = ((enemy_position[0] - my_position[0]) ** 2 + (enemy_position[1] - my_position[1]) ** 2) ** 0.5
        if enemy_distance < 100:
            self.shoot_at_player()
        else:
            self.move()


