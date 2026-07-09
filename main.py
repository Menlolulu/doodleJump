# Example file showing a basic pygame "game loop"
import pygame
pygame.init()

# configuration
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
PLAYER_SIZE = 75

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# game variables
player_x = 250
player_y = 50
player_y_speed = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move the player
    player_y += player_y_speed
    player_y_speed += 0.25
    if player_y >= SCREEN_HEIGHT - 75 - PLAYER_SIZE:
        player_y_speed = -12

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen,"yellow",(player_x,player_y,PLAYER_SIZE,PLAYER_SIZE))
    pygame.draw.rect(screen, "black", (0,SCREEN_HEIGHT - 75,SCREEN_WIDTH,25))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to ∞

pygame.quit()