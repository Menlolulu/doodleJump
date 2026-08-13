# Example file showing a basic pygame "game loop"
import math
import random
import pygame
pygame.init()

# configuration
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
PLAYER_SIZE = 75
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 25
BULLET_SPEED = 10
SCORE_FONT = pygame.font.SysFont("Tratatello", 50)

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
        if random.randint(1,3) == 1:
            self.bouncy = False
            self.breaks = True
        else:
            self.breaks = False
        if self.width == SCREEN_WIDTH:
            self.bouncy = False
            self.breaks = False
            self.x_speed = 0
    
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
            if self.breaks:
                self.teleport_up()
    
    def platform_color(self):
        if self.bouncy:
            return "#6a6a6a"
        elif self.breaks:
            return "#6F4231"
        else:
            return "black"
    
    def teleport_up(self):
        self.y += SCREEN_HEIGHT
        self.reset_platform()

    def draw(self):
        if game_y_to_screen(self.y) > SCREEN_HEIGHT and not self.width == SCREEN_WIDTH:
            self.teleport_up()
        pygame.draw.rect(screen, self.platform_color(), (
            game_x_to_screen(self.x),
            game_y_to_screen(self.y),
            self.width,
            PLATFORM_HEIGHT
        ))

class Bullet:
    def __init__(self, starting_x, starting_y):
        self.x = starting_x
        self.y = starting_y

    def move_up(self):
        self.y+= BULLET_SPEED

    def draw(self):
        pygame.draw.circle(screen,"#6a6a6a",game_point_to_screen(self.x,self.y),15)

    def try_to_kill_monster(self, monster):
        distance = math.sqrt((self.x - monster.x) ** 2 + (self.y - monster.y) ** 2)
        if distance <= 75 + 15:
            print("DIEEEEEEEEEEEE")
            # DIEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEeee
            monster.health -= 1
            print(monster.health)

class Monster:
    def __init__(self, starting_y):
        self.health = 1
        self.x = random.randint(0, SCREEN_WIDTH - 150)
        self.y = starting_y

    def draw(self):
        pygame.draw.circle(screen,"#fc1105",game_point_to_screen(self.x,self.y),75)

big_platform = Platform(30)
platforms = [
    Platform(200),
    Platform(400),
    Platform(600),
    Platform(800),
    Platform(1000),
    Platform(1200),
]

monsters = [Monster(500),Monster(1000),Monster(1500),Monster(2000)]
bullets = []

big_platform.x = 0
big_platform.width = SCREEN_WIDTH

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Bullet(player_x+50,player_y))

    # move the player
    if game_y_to_screen(player_y) < SCREEN_HEIGHT / 4:
        camera_y -= game_y_to_screen(player_y) - SCREEN_HEIGHT / 4

    player_y += player_y_speed
    player_y_speed -= 0.25

    for p in platforms:
        p.bounce_player()
        p.move_side_to_side()
    for b in bullets:
        b.move_up()
        if b.y > player_y + 1000:
            del b
            continue
        for m in monsters:
            b.try_to_kill_monster(m)
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
    for b in bullets:
        b.draw()
    for m in monsters:
        if m.health > 0:
            m.draw()
    big_platform.draw()

    score_text_image = SCORE_FONT.render(str(round(camera_y)), True, "blue")
    screen.blit(score_text_image, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to ∞

pygame.quit()