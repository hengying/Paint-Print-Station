import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from paint_station_config import Config
from paint_station_painting_layer import PaintingLayer
from paint_station_gui_layer import GuiLayer
from paint_station_brush import Brush
from paint_station_brush_dialog import BrushDialog
from paint_station_confirm_dialog import ConfirmDialog
from paint_station_open_dialog import OpenDialog
from paint_station_print import Print

class PaintStation():
    def __init__(self):
        pygame.init()
        self._config = Config()
        if self._config.win_pos_x is not None and self._config.win_pos_y is not None:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self._config.win_pos_x, self._config.win_pos_y)
        screen = pygame.display.set_mode((self._config.win_width, self._config.win_height), pygame.NOFRAME)
        if not self._config.show_cursor:
            pygame.mouse.set_visible(False)

        self.__brush = Brush()
        self._painting_layer = PaintingLayer(self, screen)
        self._gui_layer = GuiLayer(self, screen)

        self._layers = []
        self._layers.append(self._painting_layer)
        self._layers.append(self._gui_layer)

        self._brush_dialog = BrushDialog(self, screen)
        self._confirm_dialog = ConfirmDialog(self, screen)
        self._open_dialog = OpenDialog(self, screen)

        self.__font = pygame.font.Font('fonts/NotoSansCJKsc-Regular.otf', 24)

        self._print = Print()

        self._last_save_filename = None
        self._current_finger_id = None

    def run(self):
        try:
            while True:
                while True:
                    if pygame.event.peek():
                        break
                    else:
                        time.sleep(0.0167)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        raise StopIteration
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        for layer in reversed(self._layers):
                            if layer.mouse_down(e.pos) == True:
                                break
                    if e.type == pygame.MOUSEMOTION:
                        for layer in reversed(self._layers):
                            if layer.mouse_move(e.pos) == True:
                                break
                    if e.type == pygame.MOUSEBUTTONUP:
                        for layer in reversed(self._layers):
                            if layer.mouse_up(e.pos) == True:
                                break

                    if e.type == pygame.FINGERDOWN:
                        if self._current_finger_id is None:
                            self._current_finger_id = e.finger_id
                            pos = (int(e.x * self._config.win_width), int(e.y * self._config.win_height))
                            for layer in reversed(self._layers):
                                if layer.mouse_down(pos) == True:
                                    break
                    if e.type == pygame.FINGERMOTION:
                        if self._current_finger_id is not None:
                            if e.finger_id == self._current_finger_id:
                                pos = (int(e.x * self._config.win_width), int(e.y * self._config.win_height))
                                for layer in reversed(self._layers):
                                    if layer.mouse_move(pos) == True:
                                        break
                    if e.type == pygame.FINGERUP:
                        if self._current_finger_id is not None:
                            if e.finger_id == self._current_finger_id:
                                pos = (int(e.x * self._config.win_width), int(e.y * self._config.win_height))
                                for layer in reversed(self._layers):
                                    if layer.mouse_up(pos) == True:
                                        break
                                self._current_finger_id = None

                    if e.type == pygame.KEYDOWN:
                        for layer in reversed(self._layers):
                            if layer.key_down(e.key) == True:
                                break

                for layer in self._layers:
                    layer.paint()

                pygame.display.flip()
        except StopIteration:
            pass

    def load(self, painting_file):
        self._painting_layer.load_painting(painting_file)
        self._layers.pop()

    def ok(self):
        print('ok')
        self._layers.pop()
        self._do_quit()

    def cancel(self):
        self._layers.pop()

    def _do_quit(self):
        self.brush.save_brush_palette()
        self._config.save_config_file()
        pygame.quit()
        sys.exit()

    def quit(self):
        if self._painting_layer.modified_since_save:
            if self._config.display_english:
                self._confirm_dialog.show_confirm_dialog('Painting not saved, quit?', self)
            else:
                self._confirm_dialog.show_confirm_dialog('图像未保存，确定要退出吗？', self)

            self._layers.append(self._confirm_dialog)
        else:
            self._do_quit()

    @property
    def font(self):
        return self.__font

    @property
    def brush(self):
        return self.__brush

    def show_brush_dialog(self):
        self._layers.append(self._brush_dialog)

    def pop_dialog(self):
        self._layers.pop()

    def undo(self):
        self._painting_layer.undo()

    def redo(self):
        self._painting_layer.redo()

    def open(self):
        self._open_dialog.show_paintings(self._config.image_folder, self)
        self._layers.append(self._open_dialog)

    def save(self):
        self._last_save_filename = self.get_file_name()
        self._painting_layer.save(self._last_save_filename)

    def print(self):
        if self._painting_layer.modified_since_save or self._last_save_filename is None:
            self._last_save_filename = self.get_file_name()
            self._painting_layer.save(self._last_save_filename)
        self._print.print_image(self._last_save_filename)

    def get_file_name(self):
        return os.path.join(self._config.image_folder, time.strftime('%Y-%m-%d %H:%M:%S') + '.png')

    def fill_black(self):
        self._painting_layer.fill_black()

    def fill_white(self):
        self._painting_layer.fill_white()


app = PaintStation()
app.run()
#pygame.quit()
