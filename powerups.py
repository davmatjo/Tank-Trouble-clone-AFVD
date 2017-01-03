import random
import pygame


class Powerup:
    def __init__(self, screen, position):
        self.position = position
        self.type = random.choice([1, 2, 3, 4])
        self.image = pygame.image.load("Assets/powerup" + str(self.type) + ".png")
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.position
        self.screen = screen
        self.alive = True
        print("Created!")

    def draw(self):
        self.screen.blit(self.image, self.image_rect)
