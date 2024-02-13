import random
import sys

import pygame

from Sprites import Player, Enemy, Bullet, EnemyBullet
from constants import WIDTH, HEIGHT, BACKGROUND_SPEED, FPS
from helpers import get_image_path, get_sound_path, get_font_path, get_heart_frames, load_image

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
player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(Player())

# Enemy
enemy_sprites = pygame.sprite.Group()
spawn_enemy = 3000
last_enemy_spawned = 0

# Bullets
bullet_sprites = pygame.sprite.Group()
bullet_cooldown = 800
last_bullet_fired = 0

# enemy bullets
enemy_bullet_sprites = pygame.sprite.Group()
last_enemy_bullet_fired = 0
enemy_bullet_cooldown = 1600

# score
spaceship = pygame.image.load(get_image_path("spaceship.png")).convert_alpha()
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (25, 25)
score_font = pygame.font.Font(get_font_path("LuckiestGuy-Regular.ttf"), 32)
score = 0
score_text = score_font.render(f"{score}", True, "white")

# Lives

heart_frame_list = get_heart_frames(8)
heart_rect = heart_frame_list[0].get_rect()
heart_rect.bottomleft = (25, 575)
current_frame = 0
frame_delay = 200
last_frame_time = 0
lives = 3

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
title_image = load_image("spaceship_pl.png")
title_image_rect = title_image.get_rect()
title_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# sounds
pygame.mixer.music.load(get_sound_path("xeon6.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
boom = pygame.mixer.Sound(get_sound_path("boom.mp3"))
boom.set_volume(0.2)
shoot = pygame.mixer.Sound(get_sound_path("shoot.mp3"))
shoot.set_volume(0.2)

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

        # # Generate Bullets
        if keys[pygame.K_SPACE] and current_time - bullet_cooldown >= last_bullet_fired:
            bullet_sprites.add(Bullet(player_sprite.sprite.rect.center))
            last_bullet_fired = current_time
            shoot.play()

        # Spawn enemies
        if current_time - last_enemy_spawned >= spawn_enemy:
            enemy_sprites.add(Enemy(random.randint(1, 5)))
            last_enemy_spawned = current_time

        # spawn enemy bullets
        if len(enemy_sprites.sprites()) > 0:
            shooting_enemy_index = random.randint(0, len(enemy_sprites.sprites())-1)
            if current_time - enemy_bullet_cooldown >= last_enemy_bullet_fired:
                enemy_bullet_sprites.add(EnemyBullet(enemy_sprites.sprites()[shooting_enemy_index].rect.center))
                last_enemy_bullet_fired = current_time
                shoot.play()

        # # detect collisions
        if pygame.sprite.spritecollide(player_sprite.sprite, enemy_sprites, True):
            lives -= 1
            boom.play()

        if pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True):
            score += 1
            boom.play()

        if pygame.sprite.spritecollide(player_sprite.sprite, enemy_bullet_sprites, True):
            lives -= 1
            boom.play()

        # update score
        score_text = score_font.render(f"{score}", True, "white")
        if score > 5:
            spawn_enemy = 2500
        if score > 10:
            spawn_enemy = 2000
        if score > 15:
            spawn_enemy = 1500
        if score > 20:
            spawn_enemy = 1000

        # update lives
        lives_text = score_font.render(f"{lives}", True, "white")
        if lives < 1:
            game_over = True

        # update hearts
        if current_time - last_frame_time >= frame_delay:
            current_frame = (current_frame + 1) % len(heart_frame_list)
            last_frame_time = current_time

        # Draw surfaces
        screen.blit(background, background_rect_one)
        screen.blit(background, background_rect_two)
        # screen.blit(player, player_rect)

        screen.blit(spaceship, spaceship_rect)
        screen.blit(score_text, (80, 25))
        screen.blit(heart_frame_list[current_frame], heart_rect)
        screen.blit(lives_text, (80, 540))

        player_sprite.draw(screen)
        player_sprite.update()

        bullet_sprites.draw(screen)
        bullet_sprites.update()

        enemy_sprites.draw(screen)
        enemy_sprites.update()

        enemy_bullet_sprites.draw(screen)
        enemy_bullet_sprites.update()

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            lives = 3
            score = 0
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
