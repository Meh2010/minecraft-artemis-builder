import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artemis Builder")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)

player_x = 400
player_y = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= 5
    if keys[pygame.K_s]:
        player_y += 5
    if keys[pygame.K_a]:
        player_x -= 5
    if keys[pygame.K_d]:
        player_x += 5

    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 30, 30))
    pygame.display.flip()