import pygame
import sys
from pygame.locals import *
from multiplayer import start_2_player, start_3_player

pygame.init()
window_size = (800, 800)

screen = pygame.display.set_mode(window_size)
screen.fill((255, 255, 255))

try:
    back = pygame.transform.scale(pygame.image.load("maze.png").convert(), window_size)
    screen.blit(back, (0, 0))
except pygame.error:
    pass

FPS = 60
fps_clock = pygame.time.Clock()




def title_screen():
    titlescreen = True
    while titlescreen:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #Rectangles
        pygame.draw.rect(screen, (31, 196, 209), (20, 20, 760, 170))

        button("1 Player", 250, 300, 300, 60)
        button("2 Players", 250, 400, 300, 60, start_2_player)
        button("3 Players", 250, 500, 300, 60, start_3_player)
        button("Help", 680, 720, 100, 60, help_screen)

        #Text
        text_surf1, text_rect1 = text_objects("Armoured Fighting", pygame.font.SysFont('comicsansms', 70))
        text_rect1.center = ((400, 60))
        text_surf2, text_rect2 = text_objects("Vehicle Dissatisfaction", pygame.font.SysFont('comicsansms', 70))
        text_rect2.center = ((400, 140))
        screen.blit(text_surf1, text_rect1)
        screen.blit(text_surf2, text_rect2)

        pygame.display.update()
        fps_clock.tick(FPS)


def button(text, x, y, width, height, action=None):
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
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def help_screen():
    help_on = True
    while help_on:
        screen.blit(pygame.image.load("help.png", (0, 0)).convert())
        if pygame.key.get_pressed()[K_ESCAPE]:
            help_on = False



title_screen()
