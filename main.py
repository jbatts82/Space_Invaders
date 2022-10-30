###############################################################################
# Filename    : main.py
# Date        :
# Description :
###############################################################################

import pygame
import random
import math
from pygame import mixer

# py game initialization
pygame.init()

# create game screen
screen = pygame.display.set_mode((800, 600))
ship_icon = "Images/ship_sml.png"
playerPng = "Images/player.png"
enemyPng = "Images/enemy.png"
backgroundPng = "Images/bg.png"
bulletPng = "Images/bullet.png"
backgroundWav = 'Sounds/background.wav'
explosionWav = 'Sounds/explosion.wav'
laserWav = 'Sounds/laser.wav'

# Caption and Icon
pygame.display.set_caption("Space Invaders!!!!!!!!!!!!!")
icon = pygame.image.load(ship_icon)
pygame.display.set_icon(icon)

# Background
backgroundImg = pygame.image.load(backgroundPng)

# Background Sound
# mixer.music.load(backgroundWav)
# mixer.music.play(-1)

# Player
playerImg = pygame.image.load(playerPng)
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(enemyPng))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# ready = you can't see the bullet on the screen
# fire = the bullet is curretnly moving

bulletImg = pygame.image.load(bulletPng)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, ind):
    screen.blit(enemyImg[ind], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(eX, eY, bX, bY):
    distance = math.sqrt(math.pow(eX - bX, 2) + math.pow(eY - bY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True

while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # background Image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check if left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left Arrow is Pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                print("Right Arrow is Pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(laserWav)
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # if Keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Keystroke has been released ")
                playerX_change = 0

    # update player coordinates based on keypress input
    playerX += playerX_change

    # keep within screen boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736




    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound(explosionWav)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
