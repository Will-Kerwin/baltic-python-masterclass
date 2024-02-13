import random

from pygame import K_UP, K_DOWN, key
from pygame.sprite import Sprite

from constants import HEIGHT, PLAYER_SPEED, WIDTH, BULLET_SPEED
from helpers import load_image


class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("spaceship_pl.png")
        self.rect = self.image.get_rect()
        self.rect.midleft = (25, HEIGHT // 2)
        self.speed = PLAYER_SPEED

    def move_player(self):
        keys = key.get_pressed()
        # move player
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def update(self, *args, **kwargs):
        self.move_player()


class Enemy(Sprite):
    def __init__(self, enemy_type: int):
        super().__init__()
        self.image = self.select_enemy_type(enemy_type)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = self.select_lane(self.rect.height)
        self.speed = 5

    @staticmethod
    def select_enemy_type(enemy_type: int):
        match enemy_type:
            case 1:
                return load_image("spaceship_en_one.png")
            case 2:
                return load_image("spaceship_en_two.png")
            case 3:
                return load_image("spaceship_en_three.png")
            case 4:
                return load_image("spaceship_en_four.png")
            case _:
                return load_image("spaceship_en_five.png")

    @staticmethod
    def select_lane(rect_height: int):
        lane = random.randint(1, 3)
        match lane:
            case 1:
                return 0
            case 2:
                return HEIGHT // 2 - rect_height // 2
            case _:
                return HEIGHT - rect_height

    def move_enemy(self):
        self.rect.x -= self.speed

    def destroy_enemy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self, *args, **kwargs):
        self.move_enemy()
        self.destroy_enemy()


class Bullet(Sprite):
    def __init__(self, location: int):
        super().__init__()
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = BULLET_SPEED

    def move_bullet(self):
        self.rect.x += self.speed

    def destroy_bullet(self):
        if self.rect.right > WIDTH:
            self.kill()

    def update(self, *args, **kwargs):
        self.move_bullet()
        self.destroy_bullet()
