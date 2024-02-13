import os
import pygame
import random
import sys


def get_image_path(image_name: str) -> str:
    path = os.path.join("assets", "images", image_name)
    return path


def get_font_path(font_name: str) -> str:
    font = os.path.join("assets", "fonts", font_name)
    return font


# Constants
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
BACKGROUND_SPEED = 2
FPS = 60
BULLET_SPEED = 7

# Initialize Pygame
pygame.init()

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = pygame.image.load(get_image_path("space_bg.png")).convert()
background_rect_one = background.get_rect()
background_rect_one.x = 0
background_rect_two = background.get_rect()
background_rect_two.x = 800

# Player
player = pygame.image.load(get_image_path("spaceship_pl.png")).convert_alpha()
player_rect = player.get_rect()
player_rect.midleft = (25, HEIGHT // 2)

# Enemy
enemy_one = pygame.image.load(get_image_path("spaceship_en_one.png")).convert_alpha()
enemy_two = pygame.image.load(get_image_path("spaceship_en_two.png")).convert_alpha()
enemy_three = pygame.image.load(get_image_path("spaceship_en_three.png")).convert_alpha()
enemy_four = pygame.image.load(get_image_path("spaceship_en_four.png")).convert_alpha()
enemy_five = pygame.image.load(get_image_path("spaceship_en_five.png")).convert_alpha()
enemy_image_list = [enemy_one, enemy_two, enemy_three, enemy_four, enemy_five]
enemy_speed = 5
spawn_enemy = 3000
last_enemy_spawned = 0
spawned_enemies: (pygame.Surface | pygame.SurfaceType, pygame.Surface) = []

# Bullets
bullet = pygame.image.load(get_image_path("bullet.png")).convert_alpha()
bullet_list: (pygame.Surface | pygame.SurfaceType, pygame.Surface) = []
bullet_cooldown = 800
last_bullet_fired = 0

# score
spaceship = pygame.image.load(get_image_path("spaceship.png")).convert_alpha()
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (25, 25)
score_font = pygame.font.Font(get_font_path("LuckiestGuy-Regular.ttf"), 32)
score = 0
score_text = score_font.render(f"{score}", True, "white")

# Clock
clock = pygame.time.Clock()

# Title
title_font = pygame.font.Font(get_font_path("LuckiestGuy-Regular.ttf"), 72)
instructions_font = pygame.font.Font(get_font_path("LuckiestGuy-Regular.ttf"), 32)
title_text = title_font.render("SPACE ATTACK!", True, "white")
instructions_text = instructions_font.render("Press ENTER to begin", True, "white")
title_rect = title_text.get_rect()
instructions_rect = instructions_text.get_rect()
title_rect.center = (WIDTH // 2, 120)
instructions_rect.center = (WIDTH // 2, 480)
title_image = player
title_image_rect = title_image.get_rect()
title_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# Main game loop
running = True
game_over = True

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Game logic
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # background scroll
        if background_rect_one.x < -800:
            background_rect_one.x = 800
        if background_rect_two.x < -800:
            background_rect_two.x = 800
        background_rect_one.x -= BACKGROUND_SPEED
        background_rect_two.x -= BACKGROUND_SPEED

        # move player
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += PLAYER_SPEED

        # move bullets and remove when off screen
        for bullet_image, bullet_rect in bullet_list:
            bullet_rect.x += BULLET_SPEED

        bullet_list = [(bullet_image, bullet_rect) for bullet_image, bullet_rect in bullet_list if
                       bullet_rect.left < WIDTH]

        for enemy_image, enemy_rect in spawned_enemies:
            enemy_rect.x -= enemy_speed

        spawned_enemies = [(enemy_image, enemy_rect) for enemy_image, enemy_rect in spawned_enemies if
                           enemy_rect.right > 0]

        # Generate Bullets
        if keys[pygame.K_SPACE] and current_time - bullet_cooldown >= last_bullet_fired:
            bullet_image = bullet
            bullet_rect = bullet_image.get_rect()
            bullet_rect.center = player_rect.center
            bullet_list.append((bullet_image, bullet_rect))
            last_bullet_fired = current_time

        # Spawn enemies
        if current_time - last_enemy_spawned >= spawn_enemy:
            enemy_image: pygame.Surface | pygame.SurfaceType = random.choice(enemy_image_list)
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = WIDTH

            lane = random.randint(1, 3)

            match lane:
                case 1:
                    enemy_rect.y = 0
                case 2:
                    enemy_rect.y = (HEIGHT // 2 - enemy_rect.height // 2)
                case 3:
                    enemy_rect.y = HEIGHT - enemy_rect.height

            spawned_enemies.append((enemy_image, enemy_rect))
            last_enemy_spawned = current_time

        # detect collisions
        for enemy_image, enemy_rect in spawned_enemies:
            if enemy_rect.colliderect(player_rect):
                game_over = True
            for bullet_image, bullet_rect in bullet_list:
                if enemy_rect.colliderect(bullet_rect):
                    spawned_enemies.remove((enemy_image, enemy_rect))
                    bullet_list.remove((bullet_image, bullet_rect))
                    score += 1

        # update score
        score_text = score_font.render(f"{score}", True, "white")

        # Draw surfaces
        screen.blit(background, background_rect_one)
        screen.blit(background, background_rect_two)
        screen.blit(player, player_rect)

        for enemy_image, enemy_rect in spawned_enemies:
            screen.blit(enemy_image, enemy_rect)

        for bullet_image, bullet_rect in bullet_list:
            screen.blit(bullet_image, bullet_rect)

        screen.blit(spaceship, spaceship_rect)
        screen.blit(score_text, (60, 25))

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            spawned_enemies.clear()
            bullet_list.clear()
        screen.fill("black")
        screen.blit(title_text, title_rect)
        screen.blit(title_image, title_image_rect)
        screen.blit(instructions_text, instructions_rect)

    # Update display
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
