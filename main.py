import math
import random
import pygame
from pygame import mixer

# เริ่มต้นใช้งาน pygame
pygame.init()
clock = pygame.time.Clock()
game_paused = False  # ใช้เก็บสถานะของเกม False = เล่น
game_over_flag = False  # ใช้เก็บสถานะของเกมโอเวอร์
# สร้างหน้าจอ
screen = pygame.display.set_mode((800, 600))
# รูปภาพพื้นหลัง
background = pygame.image.load(r'assets/background.jpg')
# เสียงพื้นหลัง
mixer.music.stop()  # หยุดเสียงเก่าก่อน
mixer.music.load(r'assets/background.mp3')
if not mixer.music.get_busy():
    mixer.music.set_volume(0.5)  # ลดความดังลง 50%
    mixer.music.play(-1)
# ชื่อและไอคอนเกม
pygame.display.set_caption("Cat in Space")
icon = pygame.image.load(r'assets/rocket 1.png')
pygame.display.set_icon(icon)
# ผู้เล่น
playerImg = pygame.image.load(r'assets/rocket 2.png')
playerX = 370
playerY = 480
playerX_change = 0
bullet_cooldown = 0

# ศัตรู
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

def create_enemies():
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load(r'assets/enemy 1.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(1.5)
        enemyY_change.append(5)

create_enemies()

# ลูกกระสุน
# ready - คุณไม่เห็นลูกกระสุนบนหน้าจอ
# fire - ลูกกระสุนกำลังเคลื่อนที่
bulletImg = pygame.image.load(r'assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7
bullet_state = "ready"

# คะแนน
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def reset_game():
    global score_value, bulletY, bullet_state, game_over_flag, enemyX, enemyY, enemyX_change, enemyY_change
    score_value = 0
    bulletY = 480
    bullet_state = "ready"
    game_over_flag = False
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()
    create_enemies()

# วงลูปเกม
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # รูปภาพพื้นหลัง
    screen.blit(background, (0, 0))
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ถ้ามีการกดคีย์ตรวจสอบว่าเป็นซ้ายหรือขวา
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready" and bullet_cooldown == 0 and not game_over_flag:
                bulletSound = mixer.Sound(r'assets/laser.wav')
                bulletSound.set_volume(0.5)  # ลดความดังของเสียงลงครึ่งหนึ่ง
                bulletSound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_cooldown = 10  # หน่วงเวลา 10 เฟรมก่อนยิงนัดต่อไป
            if event.key == pygame.K_ESCAPE:
                if game_paused:
                    running = False  #  ออกจากเกมถ้าหยุดอยู่แล้ว
                else:
                    game_paused = True  # หยุดเกมครั้งแรก
            if event.key == pygame.K_SPACE and (game_paused or game_over_flag):
                game_paused = False  # กลับไปเล่นใหม่
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if game_over_flag:
        game_over_text()
    else:
        # การเคลื่อนที่ของผู้เล่น
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # การเคลื่อนที่ของศัตรู
        for i in range(num_of_enemies):

            # เกมโอเวอร์
            if enemyY[i] > 440:
                game_over_flag = True
                break
            
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            # การชน
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound(r'assets/Boom.wav')
                explosionSound.play()  # เล่นเสียงใหม่
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                enemyX_change[i] += 0.5  # เพิ่มความเร็วของศัตรู
                enemyY_change[i] += 0.5  # เพิ่มความเร็วของศัตรู
            enemy(enemyX[i], enemyY[i], i)

        # การเคลื่อนที่ของลูกกระสุน
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
    
    pygame.display.update()
    clock.tick(60)  # จำกัดความเร็วของเกมที่ 60 FPS