import pygame
import random
import math
import time

pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 533))
pygame.display.set_caption("Spring Girl")
icon = pygame.image.load("candy.png")
pygame.display.set_icon(icon)

# Load images
bg = pygame.image.load('background.jpg')
img_girl = pygame.image.load('girl.png')
img_choco = pygame.image.load('truffle.png')

# Initialize girl position and movement
girlx = 320
girly = 400
girlx_change = 0

# Initialize chocolates
chocos = []
num = 6
for _ in range(num):
    chocos.append({
        'x': random.randint(1, 675),
        'y': random.randint(1, 150),
        'y_change': 0.1
    })

# Initialize score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# Game over font
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("SCORE: " + str(score_val), True, (87, 58, 12))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(img_girl, (x, y))

def choco(x, y):
    screen.blit(img_choco, (x, y))

def is_collision(girlx, girly, chocox, chocoy):
    distance = math.sqrt((girlx - chocox)**2 + (girly - chocoy)**2)
    return distance < 27

# Timer function
def game_timer(start_time):
    elapsed_time = time.time() - start_time
    remaining_time = max(60 - elapsed_time, 0)  # Limit to positive values
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (87, 58, 12))
    screen.blit(timer_text, (600, 10))
    return remaining_time

running = True
choco_fall_delay = 1  # Delay between chocolates falling down
last_choco_time = time.time()  # To keep track of the last chocolate's time

start_time = time.time()  # Start time of the game
game_over = False

while running:
    screen.fill((0, 0, 255))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                girlx_change = -0.3
            if event.key == pygame.K_RIGHT:
                girlx_change = 0.3
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                girlx_change = 0

    girlx += girlx_change
    if girlx <= 2:
        girlx = 2
    elif girlx >= 675:
        girlx = 675

    if not game_over:
        current_time = time.time()
        # Add a new chocolate if enough time has passed
        if current_time - last_choco_time > choco_fall_delay:
            chocos.append({
                'x': random.randint(1, 675),
                'y': random.randint(1, 150),
                'y_change': 0.1
            })
            last_choco_time = current_time

        # Update chocolate positions and check for collision
        for choco_info in chocos:
            choco_info['y'] += choco_info['y_change']
            collision = is_collision(girlx, girly, choco_info['x'], choco_info['y'])
            if collision:
                score_val += 1
                choco_info['y'] = random.randint(50, 150)
                choco_info['x'] = random.randint(1, 675)
            choco(choco_info['x'], choco_info['y'])

        player(girlx, girly)
        show_score(textx, texty)

        # Check game timer
        remaining_time = game_timer(start_time)
        if remaining_time <= 0:
            game_over = True

    else:
        # Display game over message
        game_over_text = game_over_font.render("GAME OVER", True, (87, 58, 12))
        screen.blit(game_over_text, (200, 250))
        show_score(300, 350)

    pygame.display.update()

pygame.quit()


    

