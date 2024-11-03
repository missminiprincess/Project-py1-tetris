from copy import deepcopy
from random import choice

from src.settings import *


class Tetris:
    def __init__(self, logic):
        self.images = load_images()
        self.figure = deepcopy(choice(figures))
        self.next_figure = deepcopy(choice(figures))
        self.color = choice(self.images)
        self.next_color = choice(self.images)
        self.current_time = pg.time.get_ticks()
        self.can_be_rotated = True

        if self.figure == figures[1]:
            self.can_be_rotated = False

        self.logic = logic

    def check_borders(self, i):
        if self.figure[i].x < 0 or self.figure[i].x > FIELD_W - 1:
            return False
        elif self.figure[i].y > FIELD_H - 1 or self.logic.cup[self.figure[i].y][self.figure[i].x]:
            return False
        return True

    def move_y(self):
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].y += 1

            if not self.check_borders(i):
                self.figure = deepcopy(figure_old)
                for j in range(4):
                    self.logic.cup[figure_old[j].y][figure_old[j].x] = self.color
                self.figure, self.color = self.next_figure, self.next_color

                if self.figure == figures[1]:
                    self.can_be_rotated = False
                else:
                    self.can_be_rotated = True
                self.next_figure, self.next_color = deepcopy(choice(figures)), choice(self.images)
                break

    def rotate_figure(self):
        figure_old = deepcopy(self.figure)
        center = self.figure[0]
        for i in range(4):
            x = self.figure[i].y - center.y
            y = self.figure[i].x - center.x
            self.figure[i].x = center.x - x
            self.figure[i].y = center.y + y

            if not self.check_borders(i):
                self.figure = deepcopy(figure_old)
                break

    def update(self):
        self.move_x()

        if self.logic.rotate and self.can_be_rotated:
            self.rotate_figure()
            self.logic.rotate = False

        if pg.time.get_ticks() > self.current_time + INTERVAL - 10 * self.logic.speed:
            self.current_time = pg.time.get_ticks()
            self.move_y()

    def move_x(self):
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].x += self.logic.dx

            if not self.check_borders(i):
                self.figure = deepcopy(figure_old)
                break

    def draw(self):
        self.move_x()
        self.logic.dx = 0
        for i in range(4):
            figure_rect.x = self.figure[i].x * TILE_SIZE
            figure_rect.y = self.figure[i].y * TILE_SIZE
            self.logic.game.screen.blit(self.color, figure_rect)
            figure_rect.x = self.next_figure[i].x * TILE_SIZE + 430
            figure_rect.y = self.next_figure[i].y * TILE_SIZE + 550
            self.logic.game.screen.blit(self.next_color, figure_rect)


class GameLogic:
    def __init__(self, game):

        self.cup = [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)]
        self.game = game

        self.tetris = Tetris(self)

        self.dx = 0
        self.rotate = False

        self.speed = 0

        self.score = 0

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.dx = -1
        elif pressed_key == pg.K_RIGHT:
            self.dx = 1
        elif pressed_key == pg.K_UP:
            self.rotate = True

    def check_lines(self):
        line, lines = FIELD_H - 1, 0
        for row in range(FIELD_H - 1, -1, -1):
            count = 0
            for i in range(FIELD_W):
                if self.cup[row][i]:
                    count += 1
                self.cup[line][i] = self.cup[row][i]

            if count < FIELD_W:
                line -= 1
            else:
                lines += 1
        self.score += SCORES[lines]
        self.speed = self.score // 1000

    def update(self):
        self.tetris.update()
        self.check_lines()

    def draw_text(self):
        self.game.drop_shadow_text('TETRIS', 100, FIELD_RES[0] + 40, 50)
        self.game.drop_shadow_text('SCORE:', 80, FIELD_RES[0] + 60, 200)
        self.game.drop_shadow_text(f'{self.score}', 80, FIELD_RES[0] + 130, 300, colour=(102, 51, 204))
        self.game.drop_shadow_text('NEXT:', 80, FIELD_RES[0] + 60, 450)
        self.game.drop_shadow_text('LEVEL:', 80, FIELD_RES[0] + 60, 800)
        self.game.drop_shadow_text(f'{self.speed}', 80, FIELD_RES[0] + 130, 900, colour=(102, 51, 204))

    def draw(self):
        self.tetris.draw()
        for y, raw in enumerate(self.cup):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE_SIZE, y * TILE_SIZE
                    self.game.screen.blit(col, figure_rect)

        self.draw_text()
