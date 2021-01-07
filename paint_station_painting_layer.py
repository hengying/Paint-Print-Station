import pygame
from paint_station_layer import Layer
from paint_station_config import Config
from paint_station_history_manager import HistoryManager

class PaintingLayer(Layer):
    def __init__(self, app, surface):
        Layer.__init__(self, app, surface)
        self._config = Config()
        self._history_manager = HistoryManager()

        self._paint_pos_x = self._config.paint_pos_x
        self._paint_pos_y = self._config.paint_pos_y

        self._paint_surface = pygame.Surface((self._config.paint_width, self._config.paint_height))
        self._paint_surface.fill(self._config.canvas_init_color)
        self._add_history()

        self._draw_on = False
        self._last_pos = (0, 0)
        self._brush = self._app.brush
        self._modified_since_save = False

    def paint(self):
        self._surface.blit(self._paint_surface, (self._paint_pos_x, self._paint_pos_y))

    def mouse_down(self, pos):
        x = pos[0]
        y = pos[1]
        if x >= self._paint_pos_x \
                and x < self._paint_pos_x + self._config.paint_width \
                and y >= self._paint_pos_y \
                and y < self._paint_pos_y + self._config.paint_height:
            paint_pos = (x - self._paint_pos_x, y - self._paint_pos_y)
            self._last_pos = paint_pos
            self._draw_on = True
            self._draw_line(paint_pos, paint_pos)
            return True

        return Layer.mouse_down(self, pos)

    def mouse_move(self, pos):
        x = pos[0]
        y = pos[1]
        if self._draw_on:
            paint_pos = (x - self._paint_pos_x, y - self._paint_pos_y)
            self._draw_line(paint_pos, self._last_pos)
            self._last_pos = paint_pos
            return True

        return Layer.mouse_move(self, pos)

    def mouse_up(self, pos):
        x = pos[0]
        y = pos[1]
        if self._draw_on:
            paint_pos = (x - self._paint_pos_x, y - self._paint_pos_y)
            self._draw_line(paint_pos, self._last_pos)
            self._draw_on = False

            self._add_history()
            return True

        return Layer.mouse_up(self, pos)

    def key_down(self, key):
        if key == pygame.K_q:
            self._app.quit()
            return True

        return Layer.key_down(self, key)

    def _draw_line(self, start, end):
        self._brush.draw_line(self._paint_surface, start, end)

    def _add_history(self):
        history_surface = pygame.Surface((self._config.paint_width, self._config.paint_height))
        history_surface.blit(self._paint_surface, (0, 0, self._config.paint_width, self._config.paint_height))
        self._history_manager.add_history(history_surface)
        self._modified_since_save = True

    def undo(self):
        history_surface = self._history_manager.undo()
        if history_surface is not None:
            self._paint_surface.blit(history_surface, (0, 0, self._config.paint_width, self._config.paint_height))
            self._modified_since_save = True

    def redo(self):
        history_surface = self._history_manager.redo()
        if history_surface is not None:
            self._paint_surface.blit(history_surface, (0, 0, self._config.paint_width, self._config.paint_height))
            self._modified_since_save = True

    def save(self, file_name):
        pygame.image.save(self._paint_surface, file_name)
        self._modified_since_save = False

    def fill_black(self):
        self._paint_surface.fill((0, 0, 0))
        self._add_history()

    def fill_white(self):
        self._paint_surface.fill((255, 255, 255))
        self._add_history()

    def load_painting(self, painting_file):
        painting = pygame.image.load(painting_file)
        self._paint_surface.blit(painting, (0, 0, self._config.paint_width, self._config.paint_height))
        self._add_history()

    @property
    def modified_since_save(self):
        return self._modified_since_save