import pygame
from paint_station_dialog import Dialog
from paint_station_config import Config
from paint_station_button import Button

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class BrushDialog(Dialog):
    def __init__(self, app, surface):
        Dialog.__init__(self, app, surface)
        self.__config = Config()
        self._brush = self._app.brush

        self._is_black_color = True
        self._editor_draw_on = False
        self._test_canvas_draw_on = False

        self.__palette_start_x = 20
        self.__palette_start_y = 20

        self.__editor_x = 128
        self.__editor_y = 24
        self.__editor_cell_width = 10
        self.__editor_cell_height = 10

        self.__test_canvas_x = 358
        self.__test_canvas_y = 20
        self.__test_canvas_width = 102
        self.__test_canvas_height = 220

        self._test_canvas = pygame.Surface((self.__test_canvas_width, self.__test_canvas_height))
        self._test_canvas.fill(self.__config.canvas_init_color)
        self._last_test_canvas_pos = (0, 0)

        self.__return_button = Button(app, self._surface, (31, 262, 65, 35), '返回', app.pop_dialog, 'icons/back.png')
        self._buttons.append(self.__return_button)

        self.__clear_editor_button = Button(app, self._surface, (158, 262, 65, 35), '清空', self.clear_editor_button, 'icons/fill_white.png')
        self._buttons.append(self.__clear_editor_button)

        self.__black_color_button = Button(app, self._surface, (230, 262, 35, 35), '黑', self.black_color, 'icons/black_color.png')
        self._buttons.append(self.__black_color_button)

        self.__white_color_button = Button(app, self._surface, (272, 262, 35, 35), '白', self.white_color, 'icons/white_color.png')
        self._buttons.append(self.__white_color_button)

        self.__clear_test_canvas_button = Button(app, self._surface, (375, 262, 65, 35), '清空', self.clear_test_canvas_button, 'icons/fill_white.png')
        self._buttons.append(self.__clear_test_canvas_button)

        self.black_color()

    def paint(self):
        pygame.draw.rect(self._surface, self.__config.dialog_background_color,
                         (0, 0, self.__config.win_width, self.__config.win_height))

        b = self._app.brush
        # draw all brushes palette
        b._draw_brush_palette(self._surface, (self.__palette_start_x, self.__palette_start_x))

        # draw brushs palette grid
        grid_sx = self.__palette_start_x - 1
        grid_sy = self.__palette_start_y - 1
        for i in range(b.brush_col + 1):
            pygame.draw.line(self._surface, self.__config.brush_palette_grid_color,
                             (grid_sx + i * b.brush_cell_width, grid_sy),
                             (grid_sx + i * b.brush_cell_width, grid_sy + b.brush_cell_height * b.brush_row))

        for i in range(b.brush_row + 1):
            pygame.draw.line(self._surface, self.__config.brush_palette_grid_color,
                             (grid_sx, grid_sy + i * b.brush_cell_height),
                             (grid_sx + b.brush_cell_width * b.brush_col, grid_sy + i * b.brush_cell_height))

        # highlight current brush
        brush_index = b.current_brush_index
        c = brush_index // b.brush_row
        r = brush_index % b.brush_row
        """
        pygame.draw.rect(self._surface, self.__config.highlight_color,
                         (grid_sx + c * b.brush_cell_width,
                          grid_sy + r * b.brush_cell_height,
                          b.brush_cell_width + 1, b.brush_cell_height + 1), width = 1)
        """
        pygame.draw.rect(self._surface, self.__config.highlight_color,
                         (grid_sx + c * b.brush_cell_width - 1,
                          grid_sy + r * b.brush_cell_height - 1,
                          b.brush_cell_width + 2, b.brush_cell_height + 2), width = 2)

        # draw brush editor image
        self.__draw_brush_editor()

        # draw brush edit grid
        edit_grid_sx = self.__editor_x - 1
        edit_grid_sy = self.__editor_y - 1

        grid_color = self.__config.brush_editor_editable_grid_color
        if b.current_brush_editable:
            grid_color = self.__config.brush_editor_not_editable_grid_color

        for i in range(b.brush_width + 1):
            pygame.draw.line(self._surface, grid_color,
                             (edit_grid_sx + i * self.__editor_cell_width, edit_grid_sy),
                             (edit_grid_sx + i * self.__editor_cell_width, edit_grid_sy + self.__editor_cell_height * b.brush_width))

        for i in range(b.brush_height + 1):
            pygame.draw.line(self._surface, grid_color,
                             (edit_grid_sx, edit_grid_sy + i * self.__editor_cell_height),
                             (edit_grid_sx + self.__editor_cell_width * b.brush_height, edit_grid_sy + i * self.__editor_cell_height))

        i = b.brush_width // 2
        pygame.draw.line(self._surface, self.__config.highlight_color,
                         (edit_grid_sx + i * self.__editor_cell_width, edit_grid_sy),
                         (edit_grid_sx + i * self.__editor_cell_width,
                          edit_grid_sy + self.__editor_cell_height * b.brush_width))
        pygame.draw.line(self._surface, self.__config.highlight_color,
                         (edit_grid_sx + (i + 1) * self.__editor_cell_width, edit_grid_sy),
                         (edit_grid_sx + (i + 1) * self.__editor_cell_width,
                          edit_grid_sy + self.__editor_cell_height * b.brush_width))

        i = b.brush_height // 2
        pygame.draw.line(self._surface, self.__config.highlight_color,
                         (edit_grid_sx, edit_grid_sy + i * self.__editor_cell_height),
                         (edit_grid_sx + self.__editor_cell_width * b.brush_height,
                          edit_grid_sy + i * self.__editor_cell_height))

        pygame.draw.line(self._surface, self.__config.highlight_color,
                         (edit_grid_sx, edit_grid_sy + (i + 1) * self.__editor_cell_height),
                         (edit_grid_sx + self.__editor_cell_width * b.brush_height,
                          edit_grid_sy + (i + 1) * self.__editor_cell_height))

        # draw try canvas
        self._surface.blit(self._test_canvas, (self.__test_canvas_x, self.__test_canvas_y))

        # draw try canvas border
        pygame.draw.rect(self._surface, self.__config.test_canvas_border_color,
                         (self.__test_canvas_x, self.__test_canvas_y,
                          self.__test_canvas_width, self.__test_canvas_height), width = 1)

        Dialog.paint(self)

    def mouse_down(self, pos):
        x = pos[0]
        y = pos[1]

        b = self._app.brush
        if x >= self.__palette_start_x \
                and x < self.__palette_start_x + b.brush_col * b.brush_cell_width \
                and y >= self.__palette_start_y \
                and y < self.__palette_start_y + b.brush_row * b.brush_cell_height:
            self.set_current_brush_index((x - self.__palette_start_x) // b.brush_cell_width * b.brush_row \
                        + (y - self.__palette_start_y) // b.brush_cell_height)
            return True

        elif b.current_brush_editable \
                and x >= self.__editor_x \
                and x < self.__editor_x + self.__editor_cell_width * b.brush_width \
                and y >= self.__editor_y \
                and y < self.__editor_y + self.__editor_cell_height * b.brush_height:

            col = (x - self.__editor_x) // self.__editor_cell_width
            row = (y - self.__editor_y) // self.__editor_cell_height
            self._draw_brush_pixel(col, row)
            self._editor_draw_on = True

            return True

        elif x >= self.__test_canvas_x \
                and x < self.__test_canvas_x + self.__test_canvas_width \
                and y >= self.__test_canvas_y \
                and y < self.__test_canvas_y + self.__test_canvas_height:

            paint_pos = (x - self.__test_canvas_x, y - self.__test_canvas_y)
            self._last_test_canvas_pos = paint_pos
            self._test_canvas_draw_on = True
            self._test_canvas_draw_line(paint_pos, paint_pos)
            return True

        return Dialog.mouse_down(self, pos)

    def mouse_move(self, pos):
        x = pos[0]
        y = pos[1]

        b = self._app.brush

        if self._editor_draw_on \
                and x >= self.__editor_x \
                and x < self.__editor_x + self.__editor_cell_width * b.brush_width \
                and y >= self.__editor_y \
                and y < self.__editor_y + self.__editor_cell_height * b.brush_height:

            col = (x - self.__editor_x) // self.__editor_cell_width
            row = (y - self.__editor_y) // self.__editor_cell_height
            self._draw_brush_pixel(col, row)
            return True
        elif self._test_canvas_draw_on:
            paint_pos = (x - self.__test_canvas_x, y - self.__test_canvas_y)
            self._test_canvas_draw_line(paint_pos, self._last_test_canvas_pos)
            self._last_test_canvas_pos = paint_pos
            return True

        return Dialog.mouse_move(self, pos)

    def mouse_up(self, pos):
        x = pos[0]
        y = pos[1]

        b = self._app.brush

        if self._editor_draw_on:
            if x >= self.__editor_x \
                and x < self.__editor_x + self.__editor_cell_width * b.brush_width \
                and y >= self.__editor_y \
                and y < self.__editor_y + self.__editor_cell_height * b.brush_height:

                col = (x - self.__editor_x) // self.__editor_cell_width
                row = (y - self.__editor_y) // self.__editor_cell_height
                self._draw_brush_pixel(col, row)

            self._editor_draw_on = False
            return True
        elif self._test_canvas_draw_on:
            paint_pos = (x - self.__test_canvas_x, y - self.__test_canvas_y)
            self._test_canvas_draw_line(paint_pos, self._last_test_canvas_pos)
            self._test_canvas_draw_on = False
            return True

        return Dialog.mouse_up(self, pos)

    def _test_canvas_draw_line(self, start, end):
        self._brush.draw_line(self._test_canvas, start, end, pattern_index = 0)

    def _draw_brush_pixel(self, col, row):
        b = self._app.brush

        if b.current_brush_editable:
            if self._is_black_color:
                b.draw_brush_pixel(col, row, BLACK)
            else:
                b.draw_brush_pixel(col, row, WHITE)

    def white_color(self):
        self._is_black_color = False
        self.__black_color_button.is_checked = False
        self.__white_color_button.is_checked = True

    def black_color(self):
        self._is_black_color = True
        self.__black_color_button.is_checked = True
        self.__white_color_button.is_checked = False

    def clear_editor_button(self):
        if self._app.brush.current_brush_editable:
            self._app.brush.fill_current_brush(WHITE)

    def clear_test_canvas_button(self):
        self._test_canvas.fill(self.__config.canvas_init_color)

    def set_current_brush_index(self, current_brush_index):
        self._app.brush.current_brush_index = current_brush_index

    def __draw_brush_editor(self):
        brush_image = self._app.brush.get_current_brush_image()
        b = self._app.brush
        editor_image = pygame.transform.scale(brush_image,
                                              (b.brush_width * self.__editor_cell_width,
                                               b.brush_height * self.__editor_cell_height))
        self._surface.blit(editor_image, (self.__editor_x, self.__editor_y))

