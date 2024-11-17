import sys

from src.gameLogic import GameLogic
from src.settings import *

bground = 'src/background.png'
class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('TETRIS')
        self.screen = pg.display.set_mode(WINDOW_RES)

        self.logic = GameLogic(self)
        self.images = load_images()

        self.bg_image = pg.image.load(Path(bground)).convert_alpha()
        self.bg_image = pg.transform.scale(self.bg_image, WINDOW_RES)

    def drop_shadow_text(self, text, size, x, y, colour=(255, 255, 255), drop_colour=(0, 0, 0)):
        text_font = pg.font.SysFont('didot.ttc', size)
        drop_shadow_offset = 1 + (size // 15)
        text_bitmap = text_font.render(text, True, drop_colour)
        self.screen.blit(text_bitmap, (x + drop_shadow_offset, y + drop_shadow_offset))
        text_bitmap = text_font.render(text, True, colour)
        self.screen.blit(text_bitmap, (x, y))

    def check_events(self):
        for EVENT in pg.event.get():
            if EVENT.type == pg.QUIT or (EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_q):
                pg.quit()
                sys.exit()
            elif EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_ESCAPE:
                self.pause_screen()
            elif EVENT.type == pg.KEYDOWN:
                self.logic.control(pressed_key=EVENT.key)

    def check_game_over(self):
        for i in range(FIELD_W):
            if self.logic.cup[1][i]:
                self.game_over_screen()

    def record_screen(self):
        flag = True
        self.screen.blit(self.bg_image, self.bg_image.get_rect())
        self.drop_shadow_text('Your record:', 120, FIELD_RES[0] // 2 - 100, 100)
        self.drop_shadow_text(f'{int(get_record())}', 120, FIELD_RES[0] // 2 + 100, 200)
        self.drop_shadow_text('press S to close this window', 50, FIELD_RES[0] // 2 - 90, 600)
        while flag:
            for EVENT in pg.event.get():
                if EVENT.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_s:
                    return
            pg.display.update()

    def start_menu_screen(self):
        start = False

        while not start:
            for EVENT in pg.event.get():
                if EVENT.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_RETURN:
                    start = True
                elif EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_s:
                    self.record_screen()

            self.screen.blit(self.bg_image, self.bg_image.get_rect())
            self.drop_shadow_text('TETRIS', 120, FIELD_RES[0] // 2, 50)
            self.drop_shadow_text('press S to check your record', 50, FIELD_RES[0] // 2 - 90, 200)
            self.drop_shadow_text('press ENTER to start game', 60, FIELD_RES[0] // 2 - 100, FIELD_RES[1] // 2)
            pg.display.update()

    def pause_screen(self):
        paused = True
        pause = pg.Surface(FIELD_RES, pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.screen.blit(pause, (0, 0))
        self.drop_shadow_text('PAUSE', 90, FIELD_RES[0] // 2 - 100, 300)
        self.drop_shadow_text('press ESC to continue', 50, FIELD_RES[0] // 2 - 160, 400)
        self.drop_shadow_text('press Q to quit', 50, FIELD_RES[0] // 2 - 100, 450)
        while paused:
            for EVENT in pg.event.get():
                if EVENT.type == pg.QUIT or (EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_q):
                    pg.quit()
                    sys.exit()
                elif EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_ESCAPE:
                    paused = False

            pg.display.update()

    def game_over_screen(self):
        set_record(self.logic.score)
        pause = pg.Surface(FIELD_RES, pg.SRCALPHA)
        pause.fill((0, 0, 255, 127))
        self.screen.blit(pause, (0, 0))
        self.drop_shadow_text('YOU LOST', 90, FIELD_RES[0] // 2 - 120, 450)
        self.drop_shadow_text('press Q to quit', 50, FIELD_RES[0] // 2 - 100, 550)
        self.drop_shadow_text('press BACKSPACE to', 50, FIELD_RES[0] // 2 - 150, 700)
        self.drop_shadow_text('back to start menu', 50, FIELD_RES[0] // 2 - 120, 750)
        while True:
            for EVENT in pg.event.get():
                if EVENT.type == pg.QUIT or (EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_q):
                    pg.quit()
                    sys.exit()
                if EVENT.type == pg.KEYDOWN and EVENT.key == pg.K_BACKSPACE:
                    game.__init__()
                    game.run()
            pg.display.update()

    @staticmethod
    def draw_lines():
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(game.screen, pg.Color(0, 0, 0),
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

    def draw(self):
        self.screen.blit(self.bg_image, self.bg_image.get_rect())
        self.screen.fill(color=pg.Color(51, 51, 51), rect=(0, 0, *FIELD_RES))
        self.draw_lines()
        self.logic.draw()
        pg.display.flip()

    def run(self):
        self.start_menu_screen()
        while True:
            self.check_events()
            self.draw()
            self.logic.update()
            self.check_game_over()


if __name__ == '__main__':
    game = Game()
    game.run()

