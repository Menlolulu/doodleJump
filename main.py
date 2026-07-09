# Example file showing a basic pygame "game loop"
import random
import pygame
pygame.init()

# configuration
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
PLAYER_SIZE = 75
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 25

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# game variables
player_x = 250
player_y = 50
player_y_speed = 0
platform_x = 100

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move the player
    player_y += player_y_speed
    player_y_speed += 0.25
    if (
        player_y >= SCREEN_HEIGHT - 75 - PLAYER_SIZE and # the player is on top of the platform
        player_x <= PLATFORM_WIDTH + platform_x and # the player x is to the left of the right side of the platform
        not player_y >= SCREEN_HEIGHT - 75 and # the player is below the screen
        player_x >= platform_x - PLAYER_SIZE # the player x is to the right of the left side of the platform
    ):
        player_y_speed = -12
        platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 3
    if keys[pygame.K_RIGHT]:
        player_x += 3

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen,"yellow",(player_x,player_y,PLAYER_SIZE,PLAYER_SIZE))
    pygame.draw.rect(screen, "black", (platform_x,SCREEN_HEIGHT - 75,PLATFORM_WIDTH,PLATFORM_HEIGHT))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to ∞

pygame.quit()