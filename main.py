import pygame

pygame.init()

#Game window
screen_width = 800
screen_hight = 400

screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Game name")

#Load images
#Background image




run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()