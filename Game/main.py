import pygame
import random
import math
from pygame import mixer

pygame.init()


# Main Screen
screen = pygame.display.set_mode((600,957)) 

# load wallpaper 
wallpaper = pygame.image.load('icon/background-wallpaper.jpg')

#background music
mixer.music.load("music/background.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption(".::SPACE WAR::.")
icon = pygame.image.load('icon/icon.png')
pygame.display.set_icon(icon)

# Player 
playerImg = pygame.image.load('icon/player.png')
playerX = 268
playerY = 720
playerX_change = 0 

# enemy 
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = [] 
enemyY_change = [] 
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyType = random.randint(1,4)
    if enemyType == 1 :
        enemyImg.append(pygame.image.load('icon/enemy1.png'))
    elif enemyType == 2 :
        enemyImg.append(pygame.image.load('icon/enemy2.png'))
    elif enemyType == 3 :
        enemyImg.append(pygame.image.load('icon/enemy3.png'))
    elif enemyType == 4 :
        enemyImg.append(pygame.image.load('icon/enemy4.png'))
    enemyX.append(random.randint(100,400))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(10)



#score Text
font = pygame.font.Font('Fonts/Vazirmatn-Black.ttf', 35)  
score_value = 0 
TextX = 10 
TextY = 10



# bullet 
bulletImg = pygame.image.load('icon/bullet.png')
bulletX = 0
bulletY = 720
bulletX_change = 1 
bulletY_change = 10
bullet_state = "ready"



def game_over():
    Game_Over_font = pygame.font.Font('Fonts/Vazirmatn-Black.ttf', 60)
    Game_Over_txt = Game_Over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(Game_Over_txt,(120, 400))


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x, y))


def fire_bullet(x,y):
    screen.blit(bulletImg,(x+10,y+20))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i] ,(x,y))

def isCollision(x1,y1,x2,y2):
    # calculate distance between (x1,y1) and (x2,y2)
    distance = math.sqrt(math.pow((x2-x1),2) + math.pow((y2-y1),2))
    if distance < 30 :
        return True
    else :
        return False

# Game Frames 
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    bullet_state = "fire"
                    fire_bullet(bulletX,bulletY)
                    fire_sound = mixer.Sound("music/laser.wav")
                    fire_sound.play()

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0


    screen.fill((0,128,128))
    screen.blit(wallpaper,(0,0))

    # player movement
    playerX += playerX_change
    if playerX <= 0:
         playerX = 0 
    elif playerX >=536 :
        playerX = 536

    # enemy movement
    for i in range(num_of_enemies):
        #check Game Over
        if enemyY[i] >= 500:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=536 :
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # bullet collision 
        collision = isCollision(enemyX[i] , enemyY[i] , bulletX , bulletY )
        if collision:
            bullet_state = 'ready'
            bulletY = 720
            score_value += 1
            enemyX[i] = random.randint(100,400)
            enemyY[i] = random.randint(50,150)
            collision_sound = mixer.Sound("music/explosion.wav")
            collision_sound.play()

        enemy(enemyX[i],enemyY[i],i)
    

    # bullet movement 
    if bullet_state is 'fire':
        if bulletY <= 0 : 
            bullet_state = 'ready'
            bulletY = 720
        
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

    show_score(TextX, TextY)
    player(playerX,playerY)
    pygame.display.update()
    