from PIL import Image

# set directional constants
NORTH = 1
SOUTH = 2
EAST = 4
WEST = 8


def render(maze, width, height):
        """Renders a maze specified as a 2 dimensional list to a png file, with walls 1 pixel thick
        and corridors 1 pixel thick
        """
        print()
        space=10
        # Create a new image to render the maze
        image = Image.new("RGB", (width*(space+1)+1, height*(space+1)+1))
        position = [-space + 1, 0]
        row = 0
        for y in maze:
            position[0] += space
            position[1] = -space + 1
            for x in y:
                position[1] += space
                # Draw centre points
                for i in range(space):
                    image.putpixel((position[0], position[1]+i), (255, 255, 255))
                    for j in range(space):
                        image.putpixel((position[0]+j, position[1]+i), (255, 255, 255))
                # Draw open walls
                if not x & NORTH:
                    for i in range(space):
                        image.putpixel((position[0]+i, position[1]-1), (255, 255, 255))
                if not x & SOUTH:
                    for i in range(space):
                        image.putpixel((position[0]+i, position[1]+space), (255, 255, 255))
                if not x & EAST:
                    for i in range(space):
                        image.putpixel((position[0]+space, position[1]+i), (255, 255, 255))
                if not x & WEST:
                    for i in range(space):
                        image.putpixel((position[0]-1, position[1]+i), (255, 255, 255))
                #move the cursor
                position[1] += 1
            # move the cursor
            position[0] += 1
            row += space
        # save the image to disk
        image.save("maze.png")
