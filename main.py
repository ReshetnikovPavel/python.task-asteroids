import pygame as pg
import random
import collision
import Assets
import pygame.math
from bullet import Bullet
from player import Player
from saucer import Saucer

from asteroid import Asteroid
from score_table import ScoreTable

pygame.init()


class Game:
    def __init__(self):
        self.is_audio_on = True
        self.textures = Assets.Textures()
        self.audio = Assets.Audio()
        self.screen_width = 800
        self.screen_height = 800
        self.clock = pg.time.Clock()
        self.asteroids = []
        self.saucers = []
        self.bonuses = []
        self.count = 0
        self.is_run = True
        self.game_over = False
        self.screen = pg.display.set_mode(
            (self.screen_width, self.screen_height))
        self.player = Player(self)
        self.score = 0
        self.font = pygame.font.Font(r'Assets/Hyperspace.otf', 36)
        self.score_table = ScoreTable()
        self.draw = self.draw_game
        self.handle_events = self.handle_game_events
        self.player_name = ''

    def run(self):
        pg.display.set_caption('Asteroids')
        while self.is_run:
            self.clock.tick(60)
            self.count += 1
            if self.player.lives < 0 and not self.game_over:
                self.end_game()
            if not self.game_over:
                if self.count % 100 == 0:
                    random_number = random.choice([1, 1, 1, 2, 2, 3])
                    self.asteroids.append(Asteroid(self, random_number))
                if self.count % 1055 == 0:
                    self.saucers.append(Saucer(self))
                self.handle_controls()
                self.update()
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw()
            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_run = False
        pg.quit()

    def update(self):
        self.player.update(self)
        self.loop_object(self.player)
        for bullet in self.player.bullets:
            self.loop_object(bullet)
            bullet.update()
            if bullet.life <= 0:
                self.player.bullets.remove(bullet)

        for asteroid in self.asteroids:
            asteroid.check_bullet_collision(self)
            self.player.check_asteroid_collision(game, asteroid)
            self.loop_object(asteroid)
            asteroid.move()

        for saucer in self.saucers:
            saucer.check_asteroid_collision(self)
            saucer.check_bullet_collision(self)
            self.player.check_asteroid_collision(self, saucer)
            saucer.move(self)
            for bullet in saucer.bullets:
                self.player.check_bullet_collision(self, bullet)
                self.loop_object(bullet)
                bullet.update()
                if bullet.life <= 0:
                    saucer.bullets.remove(bullet)

        for bonus in self.bonuses:
            bonus.move(game)
            self.loop_object(bonus)

    def draw_game(self):
        score_text = self.font.render('Score: ' + str(self.score), True,
                                      (255, 255, 255))
        best_score_text = self.font.render('Best: ' + str(self.score_table.value), True,
                                           (255, 255, 255))
        lives_text = self.font.render('Lives: ' + str(self.player.lives), True,
                                      (255, 255, 255))
        self.screen.blit(score_text,
                         (self.screen_width - 500,
                          35 + score_text.get_height()))
        self.screen.blit(best_score_text,
                         (self.screen_width - 500,
                          30))
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)
        for bullet in self.player.bullets:
            bullet.draw(self.screen)
        for saucer in self.saucers:
            saucer.draw(self.screen)
            for bullet in saucer.bullets:
                bullet.draw(self.screen)
        for bonus in self.bonuses:
            bonus.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(lives_text,
                         (10,
                          30))

    def draw_death_screen(self):
        score_text = self.font.render('Score: ' + str(self.score), True,
                                      (255, 255, 255))
        best_score_text = self.font.render('Best: ' + str(self.score_table.value), True,
                                           (255, 255, 255))
        gameover_text = self.font.render('GAME OVER', True,
                                         (255, 255, 255))
        gameover_text_2 = self.font.render('Please enter your name:', True,
                                           (255, 255, 255))
        press_enter_text = self.font.render('(Press ENTER to continue)', True,
                                           (255, 255, 255))
        name_text = self.font.render(self.player_name, True, (255, 255, 255))

        self.screen.blit(score_text,
                         (self.screen_width - 500,
                          35 + score_text.get_height()))
        self.screen.blit(best_score_text,
                         (self.screen_width - 500,
                          30))
        self.screen.blit(gameover_text,
                         (game.screen_width / 2 - gameover_text.get_width() / 2,
                          game.screen_height / 2 - gameover_text.get_height() / 2 - 50))
        self.screen.blit(gameover_text_2,
                         (
                         game.screen_width / 2 - gameover_text_2.get_width() / 2,
                         game.screen_height / 2 - gameover_text.get_height() / 2 + gameover_text_2.get_height() - 50))
        self.screen.blit(name_text,
                         (
                             game.screen_width / 2 - name_text.get_width() / 2,
                             game.screen_height / 2 - gameover_text.get_height() / 2 + gameover_text_2.get_height()))
        if len(self.player_name) > 0:
            self.screen.blit(press_enter_text,
                             (
                                 game.screen_width / 2 - press_enter_text.get_width() / 2,
                                 game.screen_height - press_enter_text.get_height() - 30))

    def draw_score_table(self):
        vertical_spacing = 30
        horizontal_spacing = 100
        press_enter_text = self.font.render('(Press ENTER to restart)', True,
                                            (255, 255, 255))
        count = len(self.score_table.scores)
        for i in range(count):
            name = self.score_table.scores[i][0]
            score = str(self.score_table.scores[i][1])
            name_text = self.font.render(name, True, (255, 255, 255))
            score_text = self.font.render(score, True, (255, 255, 255))
            entry_width = name_text.get_width() + score_text.get_width() + horizontal_spacing
            self.screen.blit(name_text,
                             (
                                 game.screen_width / 2 - entry_width / 2,
                                 (vertical_spacing+name_text.get_height())*(i+1)))
            self.screen.blit(score_text,
                             (
                                 game.screen_width / 2 - entry_width / 2 + horizontal_spacing,
                                 (vertical_spacing + name_text.get_height()) * (i + 1)))
        self.screen.blit(press_enter_text,
                         (
                             game.screen_width / 2 - press_enter_text.get_width() / 2,
                             game.screen_height - press_enter_text.get_height() - 30))

    def end_game(self):
        self.game_over = True
        self.draw = self.draw_death_screen
        self.handle_events = self.handle_death_events
        print("You've met with a terrible fate, haven't you?")

    def handle_controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.turn_left()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.turn_right()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.move_forward(game)

    def handle_game_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.game_over:
                        self.player.fire(self)

    def handle_death_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.score_table.update_score(self.score, self.player_name)
                    self.draw = self.draw_score_table
                    self.handle_events = self.handle_table_events
                elif event.key == pg.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key != pg.K_SPACE and len(self.player_name) < 3:
                    self.player_name += event.unicode

    def handle_table_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.__init__()

    def loop_object(self, obj):
        if obj.position.x > self.screen_width + obj.height:
            obj.position.x = -obj.height
        elif obj.position.x < -obj.height:
            obj.position.x = self.screen_width + obj.height
        if obj.position.y > self.screen_height + obj.height:
            obj.position.y = -obj.height
        elif obj.position.y < -obj.height:
            obj.position.y = self.screen_height + obj.height


# On start
game = Game()
game.run()
