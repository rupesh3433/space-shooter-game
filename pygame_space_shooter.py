import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load assets
player_img = pygame.image.load("player_img.png")
enemy_img = pygame.image.load("enemy_img.png")
bullet_img = pygame.image.load("bullet_img.png")

# Scale images
player_img = pygame.transform.scale(player_img, (80, 80))
enemy_img = pygame.transform.scale(enemy_img, (60, 60))
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

# Player
player_rect = player_img.get_rect()
player_rect.topleft = (WIDTH // 2, HEIGHT - 80)
player_speed = 7

# Bullets
bullets = []
bullet_speed = -5
bullet_cooldown = 500  # Milliseconds between bullets
last_bullet_time = pygame.time.get_ticks()

# Enemies
enemies = []
enemy_speed = 2
enemy_spawn_time = 70  # Number of frames between enemy spawns
enemy_timer = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_time >= bullet_cooldown:
            bullet_rect = bullet_img.get_rect(center=player_rect.center)
            bullets.append(bullet_rect)
            last_bullet_time = current_time

    # Move bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > HEIGHT:
            enemies.remove(enemy)

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_time:
        enemy_rect = enemy_img.get_rect(topleft=(random.randint(0, WIDTH - 50), -50))
        enemies.append(enemy_rect)
        enemy_timer = 0

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Drawing
    screen.fill(BLACK)
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
