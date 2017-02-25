import pygame
import sys
from maze import Maze
from pygame.locals import *
from Bullet import Bullet, Mortar, WallDestroyer, Shotgun, Laser
from Tank import Tank
from maths import degcos, degsin, arctandeg, get_player_grid
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
    """
    Use
    :param afv: Armoured fighting vehicle (tank)
    :param player: player joystick object
    :return:
    """
    x_vel = player.get_axis(0)
    y_vel = player.get_axis(1)
    # Dead-zone allowance
    if not (-0.2 < x_vel < 0.2 and -0.2 < y_vel < 0.2):
        # Check the quadrant of the joystick then use arctan and add appropriate offset
        if x_vel > 0 and y_vel > 0:
            afv.set_angle(arctandeg(x_vel, -y_vel))
        if x_vel > 0 > y_vel:
            afv.set_angle(arctandeg(x_vel, -y_vel) + 360)
        if x_vel < 0 < y_vel:
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
    """
    Dual functionality - spawnpoints for tanks and powerups
    :param maze_size: Size of maze
    :param player_count: Number of possible spawnpoints to return
    :return: List of size player_count
    """

    # Calculate spacing between spawnpoints
    block_size = (window_size[0] / maze_size)

    # Initialise lists
    possible_spawnpoints = []
    tank_positions = []

    # Build a list of grid mid-points
    y_pointer = -(block_size / 2)
    for i in range(maze_size):  # Go through each possible y co-ord
        x_pointer = -(block_size / 2)
        y_pointer += block_size
        for j in range(maze_size):  # For each y co-ord, add every x and y co-ord to the list
            x_pointer += block_size
            possible_spawnpoints.append([x_pointer, y_pointer])

    # For each player, add a random coordinate to the list
    for i in range(player_count):
        tank_coordinates = randrange(0, len(possible_spawnpoints) - 1)
        tank_coordinates = possible_spawnpoints.pop(tank_coordinates)
        tank_positions.append(tank_coordinates)
    return tank_positions


def bullet_decay_and_collision_handler(t_id, bullet, tank):
    """
    Check each bullet for collisions each refresh and destroy bullets marked as dead
    :param t_id: list id of tank being checked
    :param bullet: bullet object being checked
    :param tank: list of tanks
    :return:
    """

    # Check the first bullet in the list for life
    if not tank[t_id].fired_bullets[0].alive:
        tank[t_id].fired_bullets.pop(0)

    # Allows the bullet to clear the firing tank before becoming deadly
    if bullet.lifetime > 8:
        # Checking every tank with the bullet for collisions
        for u_id in range(len(tank)):
            if tank[u_id].image_rect.colliderect(bullet.circle) and bullet.type == 0:
                bullet.alive = False
                tank[u_id].alive = False


def powerup_collision_handler(tank, powerups):
    """
    Check for tanks colliding with powerups. If a collision occurs, give tank the powerup
    :param tank: list of tanks
    :param powerups: list of powerups
    :return:
    """
    # For every tank, check every powerup
    for u_id in range(len(tank)):
        for powerup in powerups:
            # If the tank has collided, kill the powerup, give the tank the powerup type
            if tank[u_id].image_rect.colliderect(powerup.image_rect):
                powerup.alive = False
                tank[u_id].powerups = powerup.type


def special_decay_and_collision_handler(bullet, tank, game):
    """
    Very similar to normal handler, however, checks bullet type for the wall destroyer
    :param bullet: list of special bullets
    :param tank: list of tanks
    :param game: game object
    :return:
    """
    if not bullet.alive:
        # Check if the bullet is a wall destroyer
        if bullet.type == 2:
            game.background = pygame.transform.scale(pygame.image.load("maze.png"), window_size)
        special_bullets.pop(0)
    for u_id in range(len(tank)):
        if tank[u_id].image_rect.colliderect(bullet.circle) and bullet.type == 0:
            bullet.alive = False
            tank[u_id].alive = False


def fire(t_id, tanks, screen, maze):
    """
    Make the tank you want fire
    :param t_id: The list id of the tank
    :param tanks: The list of tanks
    :param screen: The screen variable
    :param maze: The maze object
    :return:
    """
    if len(tanks[t_id].fired_bullets) < 10 and tanks[t_id].alive:

        # Fire Mortar
        if tanks[t_id].powerups == 1:
            b_velocity = [degcos(tanks[t_id].angle), -degsin(tanks[t_id].angle)]
            tanks[t_id].fired_bullets.append(Mortar(screen, [tanks[t_id].position[0] + b_velocity[0] * 18,
                                                             tanks[t_id].position[1] + b_velocity[1] * 18],
                                                    b_velocity, special_bullets))

            tanks[t_id].powerups = 0

        # Fire Wall Destroyer
        elif tanks[t_id].powerups == 2:
            b_velocity = [degcos(tanks[t_id].angle) * 2, -degsin(tanks[t_id].angle) * 2]
            special_bullets.append(WallDestroyer(screen, [tanks[t_id].position[0] + b_velocity[0] * 20,
                                                             tanks[t_id].position[1] + b_velocity[1] * 20],
                                                    b_velocity, maze, window_size))
            tanks[t_id].powerups = 0

        # Fire Shotgun
        elif tanks[t_id].powerups == 3:
            b_velocity = [degcos(tanks[t_id].angle), -degsin(tanks[t_id].angle)]
            tanks[t_id].fired_bullets.append(Shotgun(screen, [tanks[t_id].position[0] + b_velocity[0] * 18,
                                                             tanks[t_id].position[1] + b_velocity[1] * 18],
                                                    b_velocity, special_bullets, tanks[t_id].angle))
            tanks[t_id].powerups = 0

        # Fire Laser
        elif tanks[t_id].powerups == 4:
            b_velocity = [degcos(tanks[t_id].angle) * 15, -degsin(tanks[t_id].angle) * 15]
            tanks[t_id].fired_bullets.append(Laser(screen, [tanks[t_id].position[0] + b_velocity[0],
                                                             tanks[t_id].position[1] + b_velocity[1]],
                                                    b_velocity, tanks[t_id].fired_bullets))
            tanks[t_id].powerups = 0

        # Fire normal Bullet
        elif not tanks[t_id].colliding:
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
            # Initialise joystick module
            pygame.joystick.init()
            # Ignore joystick if any error occurs
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
            """
            Handles running necessary functions each tick
            :return:
            """
            screen.blit(self.background, (0, 0))

            # Refresh every tank as long as it is alive
            for tank in self.tanks:
                if tank.alive:
                    tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]

            # Refresh every tanks bullets
            for i in range(2):
                for bullet in self.tanks[i].fired_bullets:
                    bullet.move()
                    bullet.draw()
                    bullet.lifespan()
                    bullet_decay_and_collision_handler(i, bullet, self.tanks)

            # Refresh the special bullets
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                special_decay_and_collision_handler(bullet, self.tanks, game)

            # Handle powerups
            self.powerup_handler()
            powerup_collision_handler(self.tanks, self.powerups)

            # Handle all player inputs
            self.handle_inputs()

            # Check for game end
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler for all players
            :return:
            """

            # Handle all movement based input
            player_1_movement(self.tanks[0], game)
            player_2_movement(self.tanks[1], game)

            # Handle other events
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                # Check for keyboard firing - does not allow holding button down
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_KP0:
                        fire(1, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.game = False

                # Check for joypad firing - does not allow holding button down
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0:
                        fire(0, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 1:
                        fire(1, self.tanks, screen, self.maze)


        def game_end_check(self):
            # Check if any number of tanks are dead
            if not (self.tanks[0].alive and self.tanks[1].alive):
                self.end_timer += 1
                # Wait 350 ticks before continuing
                if self.end_timer >= 350:
                    # If everyone is dead, just restart game
                    if not self.tanks[0].alive and not self.tanks[1].alive:
                        self.game = False
                        start_2_player(screen)
                    # If player 2 is dead
                    elif not self.tanks[1].alive:
                        self.update_score(0)
                        self.game = False
                        start_2_player(screen)
                    # If player 1 is dead
                    elif not self.tanks[0].alive:
                        self.update_score(1)
                        self.game = False
                        start_2_player(screen)

        def update_score(self, winner):
            # Update score for the winner and update window title with scores
            scores[winner] += 1
            pygame.display.set_caption("AFVD - Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]))

        def create_players(self):
            tank_positions = get_spawnpoints(self.maze_size, 2)
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))

        def powerup_handler(self):
            """
            Choose location to spawn powerups, destroy dead ones
            :return:
            """
            # Random chance for powerup to spawn
            if randrange(0, 1000) >= 998:

                # Get random spawnpoint
                chosen_point = get_spawnpoints(self.maze_size, 1)[0]

                # Check that none of the powerups exist there already
                if not any(item.position == chosen_point for item in self.powerups):
                    self.powerups.append(Powerup(screen, chosen_point))

            # Draw every alive powerup, delete dead ones
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
            # Initialise the joystick module
            pygame.joystick.init()
            # Ignore if any error occurs
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
            """
            Handles running necessary functions each tick
            :return:
            """
            screen.blit(self.background, (0, 0))

            # Refresh every tank as long as it is alive
            for tank in self.tanks:
                if tank.alive:
                    tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]

            # Refresh every tanks bullets
            for i in range(3):
                for bullet in self.tanks[i].fired_bullets:
                    bullet.move()
                    bullet.draw()
                    bullet.lifespan()
                    bullet_decay_and_collision_handler(i, bullet, self.tanks)

            # Refresh the special bullets
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                special_decay_and_collision_handler(bullet, self.tanks, game)

            # Handle powerups
            self.powerup_handler()
            powerup_collision_handler(self.tanks, self.powerups)

            # Handle all player inputs
            self.handle_inputs()

            # Check for game end
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler for all players
            :return:
            """

            # Handle all movement based input
            player_1_movement(self.tanks[0], game)
            player_2_movement(self.tanks[1], game)
            player_3_movement(self.tanks[2], game)

            # Handle other events
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                # Check for keyboard firing - does not allow holding button down
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_KP0:
                        fire(1, self.tanks, screen, self.maze)
                    if event.key == K_o:
                        fire(2, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.game = False

                # Check for joypad firing - does not allow holding button down
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0:
                        fire(0, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 1:
                        fire(1, self.tanks, screen, self.maze)
                    if event.button == 0 and event.joy == 2:
                        fire(2, self.tanks, screen, self.maze)

        def create_players(self):
            # Generate random spawnpoints
            tank_positions = get_spawnpoints(self.maze_size, 3)

            # Spawn tanks in generated spawnpoints
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))
            self.tanks.append(Tank(screen, tank_positions[2], "Player 3", "Assets/AFV3.png"))

        def game_end_check(self):
            """
            Check if the game can end, declare winner for scoring
            :return:
            """
            # Check that only one or less tanks are alive
            if self.tanks[0].alive + self.tanks[1].alive + self.tanks[2].alive <= 1:
                self.end_timer += 1
                # 300 Tick delay
                if self.end_timer >= 300:
                    # If everyone is dead, restart game no points given
                    if not self.tanks[0].alive and not self.tanks[1].alive and not self.tanks[2].alive:
                        self.game = False
                        start_3_player(screen)
                    # If tank 3 survives
                    elif not self.tanks[1].alive and not self.tanks[2].alive:
                        self.update_score(0)
                        self.game = False
                        start_3_player(screen)
                    # If tank 2 survives
                    elif not self.tanks[0].alive and not self.tanks[2].alive:
                        self.update_score(1)
                        self.game = False
                        start_3_player(screen)
                    # If tank 1 survives
                    elif not self.tanks[0].alive and not self.tanks[1]. alive:
                        self.update_score(2)
                        self.game = False
                        start_3_player(screen)

        def update_score(self, winner):
            """
            Updates scores for the winner
            :param winner: index of winner in scores list
            :return:
            """
            scores[winner] += 1
            pygame.display.set_caption("Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]) + "                   Player3: " + str(scores[2]))

        def powerup_handler(self):
            """
            Choose location to spawn powerups, destroy dead ones
            :return:
            """
            # Random chance for powerup to spawn
            if randrange(0, 1000) >= 998:

                # Get random spawnpoint
                chosen_point = get_spawnpoints(self.maze_size, 1)[0]

                # Check that none of the powerups exist there already
                if not any(item.position == chosen_point for item in self.powerups):
                    self.powerups.append(Powerup(screen, chosen_point))

            # Draw every alive powerup, delete dead ones
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

        def new_maze(self):
            my_maze = Maze(self.maze_size)
            my_maze.generate_maze()
            my_maze.render_maze()
            maze_image = pygame.image.load("maze.png").convert()
            self.background = pygame.transform.scale(maze_image, window_size)
            return my_maze

        def refresh(self):
            """
            Handles running necessary functions each tick
            :return:
            """
            screen.blit(self.background, (0, 0))

            # Refresh every tank as long as it is alive
            for tank in self.tanks:
                if tank.alive:
                    if tank == self.tanks[0]:
                        tank.move()
                    tank.draw()
                else:
                    tank.dead()
                tank.velocity = [0, 0]

            # Refresh every tanks bullets
            for i in range(2):
                for bullet in self.tanks[i].fired_bullets:
                    bullet.move()
                    bullet.draw()
                    bullet.lifespan()
                    bullet_decay_and_collision_handler(i, bullet, self.tanks)

            # Refresh the special bullets
            for bullet in special_bullets:
                bullet.move()
                bullet.draw()
                bullet.lifespan()
                special_decay_and_collision_handler(bullet, self.tanks, game)

            # Handle powerups
            self.powerup_handler()
            powerup_collision_handler(self.tanks, self.powerups)

            # Handle all player inputs
            self.handle_inputs()
            ai.calculate()

            # Check for game end
            self.game_end_check()

        def handle_inputs(self):
            """
            Input handler for all players
            :return:
            """

            # Handle all movement based input
            player_1_movement(self.tanks[0], game)

            # Handle other events
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                # Check for keyboard firing - does not allow holding button down
                if event.type == KEYDOWN:
                    if event.key == K_e:
                        fire(0, self.tanks, screen, self.maze)
                    if event.key == K_ESCAPE:
                        game.game = False

                # Check for joypad firing - does not allow holding button down
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0 and event.joy == 0:
                        fire(0, self.tanks, screen, self.maze)

        def game_end_check(self):
            # Check if any number of tanks are dead
            if not (self.tanks[0].alive and self.tanks[1].alive):
                self.end_timer += 1
                # Wait 350 ticks before continuing
                if self.end_timer >= 350:
                    # If everyone is dead, just restart game
                    if not self.tanks[0].alive and not self.tanks[1].alive:
                        self.game = False
                        start_2_player(screen)
                    # If player 2 is dead
                    elif not self.tanks[1].alive:
                        self.update_score(0)
                        self.game = False
                        start_2_player(screen)
                    # If player 1 is dead
                    elif not self.tanks[0].alive:
                        self.update_score(1)
                        self.game = False
                        start_2_player(screen)

        def update_score(self, winner):
            scores[winner] += 1
            pygame.display.set_caption("Player 1: " + str(scores[0]) + "                   Player 2: " + str(scores[1]))

        def create_players(self):
            # Generate random spawnpoints
            tank_positions = get_spawnpoints(self.maze_size, 3)

            # Spawn tanks in generated spawnpoints
            self.tanks.append(Tank(screen, tank_positions[0], "Player 1", "Assets/AFV1.png"))
            self.tanks.append(Tank(screen, tank_positions[1], "Player 2", "Assets/AFV2.png"))

        def powerup_handler(self):
            """
            Choose location to spawn powerups, destroy dead ones
            :return:
            """
            # Random chance for powerup to spawn
            if randrange(0, 1000) >= 998:

                # Get random spawnpoint
                chosen_point = get_spawnpoints(self.maze_size, 1)[0]

                # Check that none of the powerups exist there already
                if not any(item.position == chosen_point for item in self.powerups):
                    self.powerups.append(Powerup(screen, chosen_point))

            # Draw every alive powerup, delete dead ones
            for powerup in self.powerups:
                powerup.draw()
                if not powerup.alive:
                    self.powerups.pop(self.powerups.index(powerup))

    # initialising of all arrays and objects preparing for game
    game = MainGame()
    ai = Ai(game, game.tanks, screen)

    # main game loop
    while game.game:
        game.refresh()
        pygame.display.update()
        fps_clock.tick(FPS)


class Ai:
    def __init__(self, game, tanks, screen):
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
        # Get positions of both tanks
        enemy_position = self.tanks[0].position
        my_position = self.tanks[1].position

        # Break down positions into x and y
        enemy_x = enemy_position[0]
        enemy_y = enemy_position[1]
        my_x = my_position[0]
        my_y = my_position[1]

        # Get the difference in x and y for players
        x_diff = enemy_x - my_x
        y_diff = enemy_y - my_y

        # Check the 'quadrant' of the player - similar to controller movement
        if x_diff > 0:
            if y_diff > 0:
                return arctandeg(x_diff, -y_diff)
            if y_diff < 0:
                return arctandeg(x_diff, -y_diff) + 360
        if x_diff < 0:
            return arctandeg(x_diff, -y_diff) + 180
        return self.tanks[1].angle


    def shoot_at_player(self):
        # Turn to player
        self.tanks[1].set_angle(self.get_player_angle())

        # Have a small delay in firing at player
        self.fire_delay += 1
        if self.fire_delay >= 10:
            fire(1, self.tanks, self.screen, self.game.maze.maze)
            self.fire_delay = 0

    def move(self):
        # Reset fire delay
        self.fire_delay = 10

        # Get the current maze coordinates of the tank
        current_grid = get_player_grid(self.tanks[1].position, self.game.maze_size, window_size)

        # Check if a movement direction has been assigned
        if self.current_movement is None:
            # Create a list and fill it with directions walls are not.
            available_moves = []
            walls_up = self.game.maze.maze[current_grid[0]][current_grid[1]]
            if not walls_up & NORTH and not self.previous_movement == NORTH:
                available_moves.append(NORTH)
            if not walls_up & SOUTH and not self.previous_movement == SOUTH:
                available_moves.append(SOUTH)
            if not walls_up & EAST and not self.previous_movement == EAST:
                available_moves.append(EAST)
            if not walls_up & WEST and not self.previous_movement == WEST:
                available_moves.append(WEST)

            # If there is only 1 wall down which has been visited, add that direction to the list
            if not available_moves:
                available_moves.append(self.previous_movement)

            # Choose one of the directions in the list randomly
            self.current_movement = choice(available_moves)

            # Set current grid reference as previous
            self.previous_grid = current_grid

        if self.current_movement == NORTH:
            # Check if we are out of the previous grid reference yet
            if not current_grid == self.previous_grid:
                self.stop_moving()

            # Move at 2* normal player speed in north direction
            self.tanks[1].position[1] -= 2
            # Set angle to look more natural
            self.tanks[1].set_angle(90)

        if self.current_movement == SOUTH:
            # Check if we are out of the previous grid reference yet
            if not current_grid == self.previous_grid:
                self.stop_moving()

            # Move at 2* normal player speed in south direction
            self.tanks[1].position[1] += 2
            # Set angle to look more natural
            self.tanks[1].set_angle(270)

        if self.current_movement == EAST:
            # Check if we are out of the previous grid reference yet
            if not current_grid == self.previous_grid:
                self.stop_moving()

            # Move at 2* normal player speed in east direction
            self.tanks[1].position[0] += 2
            # Set angle to look more natural
            self.tanks[1].set_angle(0)

        if self.current_movement == WEST:
            # Check if we are out of the previous grid reference yet
            if not current_grid == self.previous_grid:
                self.stop_moving()

            # Move at 2* normal player speed in west direction
            self.tanks[1].position[0] -= 2
            # Set angle to look more natural
            self.tanks[1].set_angle(180)

    def stop_moving(self):
        # Allow movement of 25 ticks into area before stopping
        self.delay += 1
        if self.delay >= 25:
            # Set previous direction to prevent backtracking
            if self.current_movement == NORTH:
                self.previous_movement = SOUTH
            if self.current_movement == EAST:
                self.previous_movement = WEST
            if self.current_movement == SOUTH:
                self.previous_movement = NORTH
            if self.current_movement == WEST:
                self.previous_movement = EAST

            # Reset movement direction
            self.current_movement = None
            # Reset counter
            self.delay = 0

    def calculate(self):
        """
        Decide what to do
        :return:
        """
        # Get player positions
        enemy_position = self.tanks[0].position
        my_position = self.tanks[1].position

        # Calculate player distance
        enemy_distance = ((enemy_position[0] - my_position[0]) ** 2 + (enemy_position[1] - my_position[1]) ** 2) ** 0.5

        if enemy_distance < 100:
            self.shoot_at_player()
        else:
            self.move()


