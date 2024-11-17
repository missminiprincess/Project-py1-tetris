from pathlib import Path
import pygame as pg
from src.utils import load_images, get_record, set_record


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

