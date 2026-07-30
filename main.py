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
SCORE_FONT = pygame.font.SysFont("Tratatello", 20)

# pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# game variables
player_x = 250
player_y = SCREEN_HEIGHT / 2
player_y_speed = 0

camera_y = 0

# helper functions
def game_x_to_screen(game_x):
    return game_x

def game_y_to_screen(game_y):
    return SCREEN_HEIGHT - game_y + camera_y

def game_point_to_screen(game_x, game_y):
    return (game_x_to_screen(game_x), game_y_to_screen(game_y))

# classes
class Platform:
    def __init__(self, platform_y):
        self.width = PLATFORM_WIDTH
        self.y = platform_y
        # setting it up for the first time
        self.reset_platform()
    
    def reset_platform(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.bouncy = random.randint(1, 8) == 1
        self.x_speed = 0
        if random.randint(1,5) == 1:
            self.x_speed = 3
    
    def move_side_to_side(self):
        self.x += self.x_speed
        if self.x >= SCREEN_WIDTH - PLATFORM_WIDTH - 10:
            self.x_speed *= -1
        elif self.x <= 10:
            self.x_speed *= -1
    
    def bounce_player(self):
        global player_y_speed

        if (
            player_y <= self.y + PLAYER_SIZE and # the player is on top of the platform
            player_x <= self.width + self.x and # the player x is to the left of the right side of the platform
            not player_y <= self.y and # the player is below the screen
            player_x >= self.x - PLAYER_SIZE and # the player x is to the right of the left side of the platform
            player_y_speed < 0 # the player is falling
        ):
            if self.bouncy:
                player_y_speed = 28
            else:
                player_y_speed = 12
    
    def platform_color(self):
        if self.bouncy:
            return "#6a6a6a"
        else:
            return "black"

    def draw(self):
        if game_y_to_screen(self.y) > SCREEN_HEIGHT and not self.width == SCREEN_WIDTH:
            self.y += SCREEN_HEIGHT
            self.reset_platform()
        pygame.draw.rect(screen, self.platform_color(), (
            game_x_to_screen(self.x),
            game_y_to_screen(self.y),
            self.width,
            PLATFORM_HEIGHT
        ))

big_platform = Platform(30)
platforms = [
    Platform(200),
    Platform(400),
    Platform(600),
    Platform(800),
    Platform(1000),
    Platform(1200),
]

big_platform.x = 0
big_platform.width = SCREEN_WIDTH

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move the player
    if game_y_to_screen(player_y) < SCREEN_HEIGHT / 4:
        camera_y -= game_y_to_screen(player_y) - SCREEN_HEIGHT / 4

    player_y += player_y_speed
    player_y_speed -= 0.25

    for p in platforms:
        p.bounce_player()
        p.move_side_to_side()
    big_platform.bounce_player()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 3
    if keys[pygame.K_RIGHT]:
        player_x += 3

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen,"yellow",(game_x_to_screen(player_x),game_y_to_screen(player_y),PLAYER_SIZE,PLAYER_SIZE))
    for p in platforms:
        p.draw()
    big_platform.draw()

    score_text_image = SCORE_FONT.render(str(round(camera_y)), True, "blue")
    screen.blit(score_text_image, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to ∞

pygame.quit()