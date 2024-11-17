from pathlib import Path
import pygame as pg
rec = "record.txt"

TILE_SIZE = 53

def load_images(): # Загружает изображения блоков из директории и масштабирует их до TILE_SIZE
    files = [item for item in Path('src/blocks_images').rglob('*.png') if item.is_file()]
    images = [pg.image.load(file).convert_alpha() for file in files]
    images = [pg.transform.scale(imag, (TILE_SIZE, TILE_SIZE)) for imag in images]
    return images


def get_record(): # Читает рекорд из файла record.txt.
    with open(Path(rec)) as f:
        return f.readline()


def set_record(new_record): # Устанавливает новый рекорд, если он больше текущего.
    record = int(get_record())
    record = max(record, new_record)
    with open(Path(rec), 'w') as f:
        f.write(str(record))
