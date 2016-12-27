import random
import maze_render



def generate_maze(size):
    maze = []
    for i in range(size):
        maze.append([])
        for j in range(size):
            maze[i].append(15)
    return maze


def depth_first_search(maze, current_node_x, current_node_y):
    max_x = len(maze) - 1
    max_y = len(maze[0]) - 1
    previous_points = []
    visited = []
    visited.append((current_node_x, current_node_y))
    while True:
        print(visited)
        if len(visited) == len(maze) * len(maze[0]):
            print(len(visited), "finishing")
            return maze
        available_moves = []
        if current_node_y != 0 and (current_node_x, current_node_y - 1) not in visited:
            available_moves.append(NORTH)
        if current_node_x != max_x and (current_node_x + 1, current_node_y) not in visited:
            available_moves.append(EAST)
        if current_node_y != max_y and (current_node_x, current_node_y + 1) not in visited:
            available_moves.append(SOUTH)
        if current_node_x != 0 and (current_node_x - 1, current_node_y) not in visited:
            available_moves.append(WEST)
        if not available_moves:
            current_node = previous_points.pop()
            current_node_x, current_node_y = current_node[0], current_node[1]
        else:
            choice = random.choice(available_moves)
            print(available_moves)
            print(choice)
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

        print(maze)


maze = depth_first_search(generate_maze(20), 0, 0)
print(maze)

maze_render.render(maze, 20, 20)