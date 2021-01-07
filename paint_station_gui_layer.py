import pygame
from paint_station_layer import Layer
from paint_station_config import Config
from paint_station_button import Button

class GuiLayer(Layer):
    def __init__(self, app, surface):
        Layer.__init__(self, app, surface)
        self._config = Config()

        button_step_y = 40

        self.__undo_button = Button(app, self._surface, (8, 20 + 0 * button_step_y, 35, 35), '撤销', self.undo, 'icons/undo.png')
        self._buttons.append(self.__undo_button)

        self.__redo_button = Button(app, self._surface, (48, 20 + 0 * button_step_y, 35, 35), '重做', self.redo, 'icons/redo.png')
        self._buttons.append(self.__redo_button)

        self.__pattern0_button = Button(app, self._surface, (3, 20 + 1 * button_step_y + 8, 27, 27), '0', self.pattern0, 'icons/pattern_0.png')
        self._buttons.append(self.__pattern0_button)
        self.__pattern1_button = Button(app, self._surface, (31, 20 + 1 * button_step_y + 8, 27, 27), '1', self.pattern1, 'icons/pattern_1.png')
        self._buttons.append(self.__pattern1_button)
        self.__pattern2_button = Button(app, self._surface, (60, 20 + 1 * button_step_y + 8, 27, 27), '2', self.pattern2, 'icons/pattern_2.png')
        self._buttons.append(self.__pattern2_button)

        self.__pattern3_button = Button(app, self._surface, (3, 20 + 2 * button_step_y + 0, 27, 27), '3', self.pattern3, 'icons/pattern_3.png')
        self._buttons.append(self.__pattern3_button)
        self.__pattern4_button = Button(app, self._surface, (31, 20 + 2 * button_step_y + 0, 27, 27), '4', self.pattern4, 'icons/pattern_4.png')
        self._buttons.append(self.__pattern4_button)
        self.__pattern5_button = Button(app, self._surface, (60, 20 + 2 * button_step_y + 0, 27, 27), '5', self.pattern5, 'icons/pattern_5.png')
        self._buttons.append(self.__pattern5_button)

        self.__opaque_button = Button(app, self._surface, (16, 20 + 3 * button_step_y - 4, 27, 27), '不透明', self.opaque, 'icons/opaque.png')
        self._buttons.append(self.__opaque_button)

        self.__transparent_button = Button(app, self._surface, (46, 20 + 3 * button_step_y - 4, 27, 27), '透明', self.transparent, 'icons/transparent.png')
        self._buttons.append(self.__transparent_button)

        self.__brush_button = Button(app, self._surface, (13, 20 + 4 * button_step_y - 8, 65, 35), '笔刷', self.brush, 'icons/brush.png')
        self._buttons.append(self.__brush_button)

        #self.__fill_black_button = Button(app, self._surface, (8, 20 + 3 * button_step_y, 35, 35), '填充', self.fill_black, 'icons/fill_black.png')
        #self._buttons.append(self.__fill_black_button)

        self.__fill_white_button = Button(app, self._surface, (3, 20 + 5 * button_step_y + 6, 27, 27), '填充', self.fill_white, 'icons/fill_white.png')
        self._buttons.append(self.__fill_white_button)

        self.__openfile_button = Button(app, self._surface, (31, 20 + 5 * button_step_y + 6, 27, 27), '打开', self.open, 'icons/open.png')
        self._buttons.append(self.__openfile_button)

        self.__savefile_button = Button(app, self._surface, (60, 20 + 5 * button_step_y + 6, 27, 27), '保存', self.save, 'icons/save.png')
        self._buttons.append(self.__savefile_button)

        self.__print_button = Button(app, self._surface, (13, 20 + 6 * button_step_y, 65, 35), '打印', self.print, 'icons/print.png')
        if self._config.could_print:
            self._buttons.append(self.__print_button)

        self.__quit_button = Button(app, self._surface, (13, 300, 13, 13), '退出', app.quit, 'icons/quit_small.png')
        self._buttons.append(self.__quit_button)

        self.pattern0()
        self.opaque()

    def paint(self):
        pygame.draw.rect(self._surface, self._config.gui_background_color,
                         (0, 0, self._config.paint_pos_x, self._config.win_height))

        pygame.draw.rect(self._surface, self._config.gui_background_color,
                         (0, 0, self._config.win_width, self._config.paint_pos_y))

        pygame.draw.rect(self._surface, self._config.gui_background_color,
                         (0, self._config.paint_pos_y + self._config.paint_height,
                          self._config.win_width, self._config.win_height - self._config.paint_height))

        pygame.draw.rect(self._surface, self._config.gui_background_color,
                         (self._config.paint_pos_x + self._config.paint_width, self._config.paint_pos_y,
                          self._config.win_width - self._config.paint_pos_x - self._config.paint_width,
                          self._config.paint_height))

        Layer.paint(self)


    def undo(self):
        self._app.undo()

    def redo(self):
        self._app.redo()

    def _uncheck_all_pattern_buttons(self):
        self.__pattern0_button.is_checked = False
        self.__pattern1_button.is_checked = False
        self.__pattern2_button.is_checked = False
        self.__pattern3_button.is_checked = False
        self.__pattern4_button.is_checked = False
        self.__pattern5_button.is_checked = False

    def pattern0(self):
        self._app.brush.set_pattern(0)
        self._uncheck_all_pattern_buttons()
        self.__pattern0_button.is_checked = True

    def pattern1(self):
        self._app.brush.set_pattern(1)
        self._uncheck_all_pattern_buttons()
        self.__pattern1_button.is_checked = True

    def pattern2(self):
        self._app.brush.set_pattern(2)
        self._uncheck_all_pattern_buttons()
        self.__pattern2_button.is_checked = True

    def pattern3(self):
        self._app.brush.set_pattern(3)
        self._uncheck_all_pattern_buttons()
        self.__pattern3_button.is_checked = True

    def pattern4(self):
        self._app.brush.set_pattern(4)
        self._uncheck_all_pattern_buttons()
        self.__pattern4_button.is_checked = True

    def pattern5(self):
        self._app.brush.set_pattern(5)
        self._uncheck_all_pattern_buttons()
        self.__pattern5_button.is_checked = True

    def opaque(self):
        self.__opaque_button.is_checked = True
        self.__transparent_button.is_checked = False
        self._app.brush.set_opaque(True)

    def transparent(self):
        self.__opaque_button.is_checked = False
        self.__transparent_button.is_checked = True
        self._app.brush.set_opaque(False)

    def fill_black(self):
        self._app.fill_black()

    def fill_white(self):
        self._app.fill_white()

    def brush(self):
        self._app.show_brush_dialog()

    def open(self):
        self._app.open()

    def save(self):
        self._app.save()

    def print(self):
        self._app.print()
