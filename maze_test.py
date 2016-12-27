#from PIL import Image
import random
import pygame

NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8


class Maze:
    def __init__(self, size, spacing=20):
        self.size = size  # allows changing size of maze
        self.maze = []  # initiates maze
        self.spacing = spacing  # allows changing of white space size

    def __generate_area(self):
        """
        Generates an empty 2 dimensional array of size self.size
        :return: maze of size self.size
        """
        maze = []
        for i in range(self.size):
            maze.append([])
            for j in range(self.size):
                maze[i].append(15)
        return maze

    def generate_maze(self, current_node_x=0, current_node_y=0):
        """
        Generates a maze with size depending on what self.size is set as. Uses __generate_area()
        :param current_node_x: Starting x coordinate for DFS
        :param current_node_y: Starting y coordinate for DFS
        :return: Nothing returned
        """
        # Initialises variables for use by algorithm
        maze = self.__generate_area()
        max_x = len(maze) - 1
        max_y = len(maze[0]) - 1
        previous_points = []
        visited = [(current_node_x, current_node_y)]
        # Check if all nodes are visited
        while True:
            if len(visited) == len(maze) * len(maze[0]):
                self.maze = maze
                return
            # Fills an array with which nodes can be moved into
            available_moves = []
            if current_node_y != 0 and (current_node_x, current_node_y - 1) not in visited:
                available_moves.append(NORTH)
            if current_node_x != max_x and (current_node_x + 1, current_node_y) not in visited:
                available_moves.append(EAST)
            if current_node_y != max_y and (current_node_x, current_node_y + 1) not in visited:
                available_moves.append(SOUTH)
            if current_node_x != 0 and (current_node_x - 1, current_node_y) not in visited:
                available_moves.append(WEST)
            # Backtrack if no moves are available
            if not available_moves:
                current_node = previous_points.pop()
                current_node_x, current_node_y = current_node[0], current_node[1]
            else:
                # Choose a direction from available moves and move, knocking out walls in 2 directions and changing
                # the current node
                choice = random.choice(available_moves)
                if choice == NORTH:
                    maze[current_node_x][current_node_y] -= NORTH
                    maze[current_node_x][current_node_y - 1] -= SOUTH
                    current_node_y -= 1
                    if (current_node_x, current_node_y) not in visited:
                        visited.append((current_node_x, current_node_y))
                    previous_points.append((current_node_x, current_node_y))

                elif choice == EAST:
                    maze[current_node_x][current_node_y] -= EAST
                    maze[current_node_x + 1][current_node_y] -= WEST
                    current_node_x += 1
                    if (current_node_x, current_node_y) not in visited:
                        visited.append((current_node_x, current_node_y))
                    previous_points.append((current_node_x, current_node_y))

                elif choice == SOUTH:
                    maze[current_node_x][current_node_y] -= SOUTH
                    maze[current_node_x][current_node_y + 1] -= NORTH
                    current_node_y += 1
                    if (current_node_x, current_node_y) not in visited:
                        visited.append((current_node_x, current_node_y))
                    previous_points.append((current_node_x, current_node_y))

                elif choice == WEST:
                    maze[current_node_x][current_node_y] -= WEST
                    maze[current_node_x - 1][current_node_y] -= EAST
                    current_node_x -= 1
                    if (current_node_x, current_node_y) not in visited:
                        visited.append((current_node_x, current_node_y))
                    previous_points.append((current_node_x, current_node_y))

    def render_maze(self):
        """
        Renders a maze specified as a 2 dimensional list to a png file, with walls 1 pixel thick
        and corridors 1 pixel thick
        """
        print()
        space = self.spacing
        # Create a new image to render the maze
        position = [-space + 1, 0]
        row = 0
        for y in self.maze:
            position[0] += space
            position[1] = -space + 1
            for x in y:
                position[1] += space
                # Draw centre points
                for i in range(space):
                    image.putpixel((position[0], position[1] + i), (255, 255, 255))
                    for j in range(space):
                        image.putpixel((position[0] + j, position[1] + i), (255, 255, 255))
                # Draw open walls
                if not x & NORTH:
                    pygame.draw.rect((position[0] + i, position[1] - 1), 5, 1)
                if not x & SOUTH:
                    pygame.draw.Rect((position[0] + i, position[1] + space), )
                if not x & EAST:
                    pygame.draw.Rect((position[0] + space, position[1] + i), )
                if not x & WEST:
                    pygame.draw.Rect((position[0] - 1, position[1] + i), )
                # move the cursor
                position[1] += 1
            # move the cursor
            position[0] += 1
            row += space
        # save the image to disk
        image.save("maze.png")

my_maze = Maze(5)
my_maze.generate_maze()
print(my_maze.maze)