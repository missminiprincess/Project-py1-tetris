from pathlib import Path

import pygame as pg

TILE_SIZE = 53
FIELD = FIELD_W, FIELD_H = 10, 19
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

WINDOW_RES = WINDOW_W, WINDOW_H = FIELD_RES[0] * 1.65, FIELD_RES[1]

SCORES = {
    0: 0,
    1: 100,
    2: 300,
    3: 700,
    4: 1500
}

INTERVAL = 200

SHAPES = [
    [(-1, 0), (-2, 0), (0, 0), (1, 0)],
    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, -1)],
    [(0, 0), (0, -1), (0, 1), (1, -1)],
    [(0, 0), (0, -1), (0, 1), (-1, 0)]
]

figures = [[pg.Rect(x + FIELD_W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in SHAPES]
figure_rect = pg.Rect(0, 0, TILE_SIZE - 4, TILE_SIZE - 4)


def load_images():
    files = [item for item in Path('src/blocks_images').rglob('*.png') if item.is_file()]
    images = [pg.image.load(file).convert_alpha() for file in files]
    images = [pg.transform.scale(imag, (TILE_SIZE, TILE_SIZE)) for imag in images]
    return images


def get_record():
    with open(Path("record.txt")) as f:
        return f.readline()


def set_record(new_record):
    record = int(get_record())
    record = max(record, new_record)
    with open(Path("record.txt"), 'w') as f:
        f.write(str(record))
