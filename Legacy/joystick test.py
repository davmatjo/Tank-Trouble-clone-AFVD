import pygame

pygame.init()
pygame.joystick.init()

clock = pygame.time.Clock()
p1_control = pygame.joystick.Joystick(0)
p1_control.init()
print(p1_control.get_name())
print(p1_control.get_axis(0))
print(p1_control.get_hat(0))
while True:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    x = p1_control.get_button(0)
    if x == 1:
        print("Yes", end="\r")
    clock.tick(20)