import random
import pygame.math as m
import pygame as pg
import vectorRandom

import collision
from bullet import Bullet
from bonus import Bonus


class Saucer:
    def __init__(self, game, spawn_point=None, direction=None):
        self.texture = game.textures.saucer
        self.width = self.texture.get_width()
        self.height = self.texture.get_height()
        self.bullets = []
        if spawn_point is None:
            self.spawn_point = random.choice(
                [(random.randrange(0, game.screen_width - self.width),
                  random.choice(
                      [-1 * self.height - 5, game.screen_height + 5])),
                 (random.choice([-1 * self.width - 5, game.screen_width + 5]),
                  random.randrange(0, game.screen_height - self.height))])
        else:
            self.spawn_point = spawn_point
        x, y = self.spawn_point
        self.position = m.Vector2(x, y)
        if direction is None:
            self.direction = m.Vector2(
                1 if x < game.screen_width // 2 else -1,
                1 if y < game.screen_height // 2 else -1)
        else:
            self.direction = direction
        self.velocity = m.Vector2(self.direction.x * random.randrange(1, 3),
                                  self.direction.y * random.randrange(1, 3))
        self.head = self.position

    def move(self, game):
        if self.position.x > game.screen_width \
                or self.position.y > game.screen_height:
            self.move_towards_center(game)
        elif game.count % game.level_info.saucer_fire_timing == 0:
            self.change_direction()
            self.fire(game)
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    def fire(self, game):
        direction = (game.player.position - self.position).normalize()
        if game.is_audio_on:
            pg.mixer.Sound.play(game.audio.fire)
        bullet = Bullet(self, direction, True)
        bullet.velocity /= 2
        self.bullets.append(bullet)

    def change_direction(self):
        self.direction = m.Vector2(vectorRandom.make_rand_vector())
        self.velocity = m.Vector2(self.direction.x * random.randrange(1, 3),
                                  self.direction.y * random.randrange(1, 3))

    def check_asteroid_collision(self, game, asteroid):
        if collision.check_collision(self, asteroid):
            asteroid.explode(game)
            self.explode(game)

    def check_bullet_collision(self, game, bullet):
        if collision.check_collision(self, bullet):
            self.explode(game)
            game.score += 5 * game.get_score_multiplier()
            game.player.bullets.remove(bullet)

    def explode(self, game):
        if self in game.saucers:
            game.saucers.remove(self)
            game.bonuses.append(Bonus(game, self.position, self.direction))
        if game.is_audio_on:
            pg.mixer.Sound.play(game.audio.explodes[2])

    def move_towards_center(self, game):
        center = m.Vector2(game.screen_width / 2, game.screen_height / 2)
        rand_vector = m.Vector2(vectorRandom.make_rand_vector())
        coefficient = 0.5
        rand_vector = m.Vector2(rand_vector.x * coefficient,
                                rand_vector.y * coefficient)
        self.direction = (center - self.position + rand_vector).normalize()*0.1
        self.velocity = m.Vector2(self.direction.x * random.randrange(1, 3),
                                  self.direction.y * random.randrange(1, 3))

    def draw(self, window):
        window.blit(self.texture, self.position)
