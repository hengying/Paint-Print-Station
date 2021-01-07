import os
import pygame
from paint_station_config import Config
from paint_station_paper_pattern import PaperPattern

BRUSH_WIDTH = 21
BRUSH_HEIGHT = 21

# 给笔刷之间留一个像素的间隔，便于在笔刷对话框中绘制所有笔刷
BRUSH_CELL_WIDTH = 22
BRUSH_CELL_HEIGHT = 22

BRUSH_COL = 4
BRUSH_ROW = 10

BRUSH_IMG_FILE = 'brush/brush.png'

WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)

# 0~8 could not be edited
LEASE_EDITABLE_BRUSH_INDEX = 9

class Brush():
    def __init__(self):
        self._config = Config()
        self._paper_pattern = PaperPattern()
        self.__current_brush_image = None
        self.__masked_brush = None
        self._load_brush()
        self._half_brush_width = BRUSH_WIDTH // 2
        self._half_brush_height = BRUSH_HEIGHT // 2
        self._is_opaque = True

    def generate_default_brushes(self):
        self.__all_brushes_surface = pygame.Surface((BRUSH_CELL_WIDTH * BRUSH_COL, BRUSH_CELL_HEIGHT * BRUSH_ROW))
        pygame.draw.rect(self.__all_brushes_surface, (255, 255, 255),
                         (0, 0, BRUSH_CELL_WIDTH * BRUSH_COL, BRUSH_CELL_HEIGHT * BRUSH_ROW))

        radius = [0, 1, 2, 3, 4, 5, 6, 8, 10]
        for i in range(BRUSH_COL):
            for j in range(BRUSH_ROW):
                c = i * BRUSH_ROW + j
                if c < len(radius):
                    pygame.draw.ellipse(self.__all_brushes_surface, (0, 0, 0),
                                        (i * BRUSH_CELL_WIDTH + BRUSH_WIDTH / 2 - radius[c],
                                         j * BRUSH_CELL_HEIGHT + BRUSH_HEIGHT / 2 - radius[c],
                                         radius[c] * 2 + 1,
                                         radius[c] * 2 + 1))
                else:
                    pygame.draw.ellipse(self.__all_brushes_surface, (0, 0, 0),
                                        (i * BRUSH_CELL_WIDTH + BRUSH_WIDTH / 2,
                                         j * BRUSH_CELL_HEIGHT + BRUSH_HEIGHT / 2,
                                         1,
                                         1))
        self.save_brush_palette()

    def _load_brush(self):
        if os.path.exists(BRUSH_IMG_FILE):
            self.__all_brushes_surface = pygame.image.load(BRUSH_IMG_FILE)
        else:
            self.generate_default_brushes()

        self.current_brush_index = self._config.saved_current_brush_index

    def save_brush_palette(self):
        pygame.image.save(self.__all_brushes_surface, BRUSH_IMG_FILE)

    def _draw_brush_palette(self, surface, pos):
        rect = self.__all_brushes_surface.get_rect()
        rect[0] = pos[0]
        rect[1] = pos[1]
        surface.blit(self.__all_brushes_surface, rect)

    @property
    def brush_width(self):
        return BRUSH_WIDTH

    @property
    def brush_height(self):
        return BRUSH_HEIGHT

    @property
    def brush_cell_width(self):
        return BRUSH_CELL_WIDTH

    @property
    def brush_cell_height(self):
        return BRUSH_CELL_HEIGHT

    @property
    def brush_col(self):
        return BRUSH_COL

    @property
    def brush_row(self):
        return BRUSH_ROW

    @property
    def current_brush_editable(self):
        return self.__current_brush_index >= LEASE_EDITABLE_BRUSH_INDEX

    @property
    def current_brush_index(self):
        return self.__current_brush_index

    @current_brush_index.setter
    def current_brush_index(self, value):
        if value < 0 or value >= self.brush_row * self.brush_col:
            print('out of boundery:', value)
            raise Exception
        self.__current_brush_index = value

        self._config.saved_current_brush_index = value

        # prepare current_brush_image
        self.__current_brush_image = pygame.Surface((BRUSH_WIDTH, BRUSH_HEIGHT))
        c = self.__current_brush_index // self.brush_row
        r = self.__current_brush_index % self.brush_row
        self.__current_brush_image.blit(self.__all_brushes_surface,
                                        (0, 0),
                                        (c * BRUSH_CELL_WIDTH, r * BRUSH_CELL_HEIGHT, BRUSH_WIDTH, BRUSH_HEIGHT))

        self._update_real_brush()

    def _update_real_brush(self):
        self.__masked_brush = pygame.Surface((BRUSH_WIDTH, BRUSH_HEIGHT))
        self.__masked_brush.blit(self.__current_brush_image, (0, 0))
        self.__masked_brush.set_colorkey(WHITE)

    def draw_brush_pixel(self, col, row, color):
        self.__current_brush_image.set_at((col, row), color)
        self.update_current_brush_into_palette()
        self._update_real_brush()

    def fill_current_brush(self, color):
        self.__current_brush_image.fill(color)
        self.update_current_brush_into_palette()
        self._update_real_brush()

    def get_current_brush_image(self):
        return self.__current_brush_image

    def draw_brush(self, surface, pos, pattern_index = None):
        paper_pattern = self._paper_pattern.get_pattern(pattern_index)

        pattern_pos_x = pos[0] % self._paper_pattern.step_h
        pattern_pos_y = pos[1] % self._paper_pattern.step_v

        partial_pattern = pygame.Surface((BRUSH_WIDTH, BRUSH_HEIGHT))
        partial_pattern.blit(paper_pattern, (-self._paper_pattern.step_h-pattern_pos_x,
                                -self._paper_pattern.step_v -pattern_pos_y, BRUSH_WIDTH, BRUSH_HEIGHT))

        brush_mask = pygame.mask.from_surface(self.__masked_brush)
        tmp_surface = pygame.Surface((BRUSH_WIDTH, BRUSH_HEIGHT))
        if self._is_opaque:
            pen = brush_mask.to_surface(surface=tmp_surface, \
                                       setsurface=partial_pattern,
                                        unsetcolor=PURPLE,
                                        dest=(0, 0))
            pen.set_colorkey(PURPLE)
        else:
            pen = brush_mask.to_surface(surface=tmp_surface, \
                                       setsurface=partial_pattern,
                                        unsetcolor=WHITE,
                                        dest=(0, 0))
            pen.set_colorkey(WHITE)

        surface.blit(pen, (pos[0] - self._half_brush_width,
                                         pos[1] - self._half_brush_height))

    def draw_line(self, surface, start, end, pattern_index = None):
        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]

        xp = x1
        yp = y1

        dx = (x2 - x1) if (x2 - x1 >= 0) else (x1 - x2)
        dy = -((y2 - y1) if (y2 - y1 >= 0) else (y1 - y2))

        x_inc = 1 if x1 < x2 else -1
        y_inc = 1 if y1 < y2 else -1

        esp = dx + dy

        while True:
            self.draw_brush(surface, (xp, yp), pattern_index)

            e2 = 2 * esp

            if e2 >= dy:
                if xp == x2:
                    break

                esp += dy
                xp += x_inc

            if e2 <= dx:
                if yp == y2:
                    break

                esp += dx
                yp += y_inc

    def set_pattern(self, pattern_index):
        self._paper_pattern.set_pattern(pattern_index)

    def set_opaque(self, is_opaque):
        self._is_opaque = is_opaque

    def update_current_brush_into_palette(self):
        c = self.__current_brush_index // self.brush_row
        r = self.__current_brush_index % self.brush_row
        self.__all_brushes_surface.blit(self.__current_brush_image,
                                        (c * BRUSH_CELL_WIDTH, r * BRUSH_CELL_HEIGHT),
                                        self.__current_brush_image.get_rect())
