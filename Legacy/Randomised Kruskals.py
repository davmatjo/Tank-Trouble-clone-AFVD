__author__ = 'jonesd1'
# Generate( Maze m )
#     While (# Walls Down < Total # Cells - 1)
#        Choose random cell current
#        Choose random neighbor of current that has a wall up between it and current
#        If such a neighbor exists
#           Find the labels of current and neighbor
#           If they are different, union them, knock down the wall, and add to # Walls Down

#N, S, E, W
#1, 1, 1, 1 = 15

NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8

def generate_maze(size):
    maze = []
    for i in range(size):
        maze.append([])
        for j in range(size):
            maze[i].append([15])
    return maze

def randomised_kruskals(size):
    maze = generate_maze(size)



