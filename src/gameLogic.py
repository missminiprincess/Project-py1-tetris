from copy import deepcopy
from random import choice

from src.settings import *


class Tetris:
    def __init__(self, logic): # Инициализирует объект Tetris, устанавливает начальные параметры фигуры и цвет, загружает изображения
        self.images = load_images() # Загружает изображения для фигур
        self.figure = deepcopy(choice(figures)) # Выбирает случайную текущую фигуру
        self.next_figure = deepcopy(choice(figures)) # Выбирает следующую фигуру
        self.color = choice(self.images)  # Определяет цвет текущей фигуры
        self.next_color = choice(self.images) # Определяет цвет следующей фигуры
        self.current_time = pg.time.get_ticks() # Сохраняет текущее время для обновлений
        self.can_be_rotated = True # Определяет возможность вращения фигуры

        if self.figure == figures[1]:# Проверяет, может ли быть возможным вращение фигуры (например, некоторые фигуры не могут вращаться)
            self.can_be_rotated = False

        self.logic = logic

    def check_borders(self, i):
        """ Проверяет, находится ли текущая фигура за границами игрового поля|i указывает, какой из 4 блоков текущей фигуры проверяется.
Позволяет поочередно проверить каждый блок на выход за границы или столкновение."""

        if self.figure[i].x < 0 or self.figure[i].x > FIELD_W - 1:
            return False # Фигура вышла за левую или правую границу
        elif self.figure[i].y > FIELD_H - 1 or self.logic.cup[self.figure[i].y][self.figure[i].x]:
            return False # Фигура вышла за нижнюю границу или столкнулась с другой фигурой
        return True # Фигура находится в допустимых границах

    def move_y(self): # Перемещает фигуру вниз по игровому полю
        figure_old = deepcopy(self.figure) # Сохраняем текущее положение фигуры
        for i in range(4):
            self.figure[i].y += 1 # Перемещение вниз на одну единицу

            if not self.check_borders(i): # Проверка на выход за границы
                self.figure = deepcopy(figure_old) # Восстанавливаем положение фигуры
                for j in range(4):
                    self.logic.cup[figure_old[j].y][figure_old[j].x] = self.color # Записываем цвет фигуры на поле
                self.figure, self.color = self.next_figure, self.next_color # Устанавливаем новую текущую фигуру

                if self.figure == figures[1]: # Проверяем, можно ли вращать новую фигуру
                    self.can_be_rotated = False
                else:
                    self.can_be_rotated = True
                self.next_figure, self.next_color = deepcopy(choice(figures)), choice(self.images) # Генерируем новую следующую фигуру
                break

    def rotate_figure(self): # Вращает фигуру вокруг её центра
        figure_old = deepcopy(self.figure) # Сохраняем текущее положение фигуры
        center = self.figure[0] # Центр вращения - первая точка фигуры
        for i in range(4): # Вычисление новых координат для вращения
            x = self.figure[i].y - center.y
            y = self.figure[i].x - center.x
            self.figure[i].x = center.x - x
            self.figure[i].y = center.y + y

            if not self.check_borders(i): # Проверка на выход за границы после вращения
                self.figure = deepcopy(figure_old) # Восстанавливаем положение фигуры
                break # Прерываем вращение, если выход за границы

    def update(self): # Обновляет состояние игры, обрабатывает ввод и перемещение фигуры
        self.move_x() # Перемещаем фигуру по оси X

        if self.logic.rotate and self.can_be_rotated: # Проверка на вращение фигуры с учетом пользовательского ввода
            self.rotate_figure() # Вращаем фигуру
            self.logic.rotate = False # Сбрасываем флаг вращения

        if pg.time.get_ticks() > self.current_time + INTERVAL - 10 * self.logic.speed: # Проверяем, прошло ли время, чтобы переместить фигуру вниз
            self.current_time = pg.time.get_ticks() # Сохраняем текущее время
            self.move_y() # Перемещаем фигуру вниз

    def move_x(self):# Перемещает фигуру влево или вправо в зависимости от пользовательского ввода
        figure_old = deepcopy(self.figure) # Сохраняем текущее положение
        for i in range(4):
            self.figure[i].x += self.logic.dx # Применяем смещение по оси X

            if not self.check_borders(i): # Проверяем на выход за границы
                self.figure = deepcopy(figure_old) # Восстанавливаем фигуру
                break  # Прерываем цикл

    def draw(self): # Отрисовывает текущую и следующую фигуры на экране
        self.move_x()  # Обновляем смещение по оси X
        self.logic.dx = 0 # Сбрасываем смещение по X
        for i in range(4):
            # Отрисовка текущей фигуры на экране
            figure_rect.x = self.figure[i].x * TILE_SIZE
            figure_rect.y = self.figure[i].y * TILE_SIZE
            self.logic.game.screen.blit(self.color, figure_rect)
            # Отрисовка следующей фигуры
            figure_rect.x = self.next_figure[i].x * TILE_SIZE + 430
            figure_rect.y = self.next_figure[i].y * TILE_SIZE + 550
            self.logic.game.screen.blit(self.next_color, figure_rect)


class GameLogic:
    def __init__(self, game: 'Game'): # Инициализирует логику игры и игровое поле
        self.cup = [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)] # Создает игровое поле
        self.game = game # Сохраняет ссылку на основной объект игры

        self.tetris = Tetris(self) # Создает объект Tetris, передавая ему логику

        self.dx = 0
        self.rotate = False

        self.speed = 0

        self.score = 0

    def control(self, pressed_key: int): # Обрабатывает ввод пользователя для управления движением фигуры
        if pressed_key == pg.K_LEFT:
            self.dx = -1
        elif pressed_key == pg.K_RIGHT:
            self.dx = 1
        elif pressed_key == pg.K_UP:
            self.rotate = True

    def check_lines(self): # Проверяет заполненные линии и удаляет их, обновляет счет
        line, lines = FIELD_H - 1, 0
        for row in range(FIELD_H - 1, -1, -1):
            count = 0 # Счетчик заполненных ячеек в строке
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

    def update(self):    # Обновляет состояние игры Tetris и проверяет, были ли заполнены линии
        self.tetris.update()  # Вызывает метод обновления состояния фигуры в классе Tetris
        self.check_lines()  # Проверяет заполненные линии на игровом поле и обновляет счет

    def draw_text(self):# Отрисовывает текстовые элементы на экране
        self.game.drop_shadow_text('TETRIS', 100, FIELD_RES[0] + 40, 50) # Название игры
        self.game.drop_shadow_text('SCORE:', 80, FIELD_RES[0] + 60, 200)  # Заголовок для счета
        self.game.drop_shadow_text(f'{self.score}', 80, FIELD_RES[0] + 130, 300, colour=(102, 51, 204))  # Текущий счет
        self.game.drop_shadow_text('NEXT:', 80, FIELD_RES[0] + 60, 450) # Заголовок для следующей фигуры
        self.game.drop_shadow_text('LEVEL:', 80, FIELD_RES[0] + 60, 800) # Заголовок для уровня
        self.game.drop_shadow_text(f'{self.speed}', 80, FIELD_RES[0] + 130, 900, colour=(102, 51, 204)) # Текущий уровень

    def draw(self):# Отрисовывает текущие элементы игры и текстовую информацию на экране# Отрисовывает текущие элементы игры и текстовую информацию на экране
        self.tetris.draw() # Вызывает метод отрисовки фигур из класса Tetris
        for y, raw in enumerate(self.cup): # Проходит по каждой строке (y) и колонке (x) игрового поля
            for x, col in enumerate(raw):
                if col: # Если в текущей ячейке есть цвет (фигура)
                    figure_rect.x, figure_rect.y = x * TILE_SIZE, y * TILE_SIZE # Устанавливает позицию прямоугольника по координатам
                    self.game.screen.blit(col, figure_rect) # Отрисовывает цвет на экране в установленной позиции

        self.draw_text() # Вызывает метод draw_text для отрисовки текстовой информации

