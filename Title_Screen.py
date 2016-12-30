import pygame
import sys
from pygame.locals import *
from multiplayer import start_2_player, start_3_player

pygame.init()
window_size = (800, 800)

screen = pygame.display.set_mode(window_size)
screen.fill((255, 255, 255))

# The try clause exists to prevent a crash incase the maze image is missing
try:
    back = pygame.transform.scale(pygame.image.load("maze.png").convert(), window_size)
    screen.blit(back, (0, 0))
except pygame.error:
    pass

# Loading the help screen into memory pre-game
help_image = pygame.transform.scale(pygame.image.load("help.png").convert(), window_size)

FPS = 60
fps_clock = pygame.time.Clock()


def title_screen():
    titlescreen = True
    while titlescreen:
        pygame.display.set_caption("AFVD")

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # Draw rectangles and buttons each refresh
        pygame.draw.rect(screen, (31, 196, 209), (20, 20, 760, 170))

        button("1 Player", 250, 300, 300, 60)
        button("2 Players", 250, 400, 300, 60, start_2_player)
        button("3 Players", 250, 500, 300, 60, start_3_player)
        button("Help", 680, 720, 100, 60, help_screen)

        # Draw extra text each refresh
        text_surf1, text_rect1 = text_objects("Armoured Fighting", pygame.font.SysFont('comicsansms', 70))
        text_rect1.center = ((400, 60))
        text_surf2, text_rect2 = text_objects("Vehicle Dissatisfaction", pygame.font.SysFont('comicsansms', 70))
        text_rect2.center = ((400, 140))
        screen.blit(text_surf1, text_rect1)
        screen.blit(text_surf2, text_rect2)

        pygame.display.update()
        fps_clock.tick(FPS)


def button(text, x, y, width, height, action=None):
    """
    Function that allows creation of buttons with text in more easily
    :param text: text to go in the button
    :param x: x co-ordinate of the left side of the button
    :param y: y co-ordinate (from the top) of the to side of the button
    :param width: self-explanatory
    :param height: self-explanatory
    :param action: pass function in for button to run when clicked
    :return: nil
    """
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.draw.rect(screen, (120, 198, 220), (x, y, width, height))
        if click[0] == 1 and action != None:
            action(screen)
    else:
        pygame.draw.rect(screen, (31, 196, 209), (x, y, width, height))

    text_surf, text_rect = text_objects(text, pygame.font.Font("arial.ttf", 40))
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


def text_objects(text, font):
    """
    :param text: text to be written to surface
    :param font: font
    :return: text surface ready for blitting onto screen, along with co-ordinates of rectangle boundaries
    """
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def help_screen(screen):
    help_on = True
    while help_on:
        screen.blit(help_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    help_on = False

        pygame.display.update()
        fps_clock.tick(FPS)
    try:
        back = pygame.transform.scale(pygame.image.load("maze.png").convert(), window_size)
        screen.blit(back, (0, 0))
    except pygame.error:
        pass

title_screen()
