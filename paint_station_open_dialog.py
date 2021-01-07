import glob
import pygame
from paint_station_dialog import Dialog
from paint_station_config import Config
from paint_station_button import Button

class OpenDialog(Dialog):
    def __init__(self, app, surface):
        Dialog.__init__(self, app, surface)
        self._config = Config()

        button_step_y = 40

        self._previous_button = Button(app, self._surface, (8, 20 + 2 * button_step_y, 35, 35), '前', self.previous_painting, 'icons/previous.png')

        self._next_button = Button(app, self._surface, (48, 20 + 2 * button_step_y, 35, 35), '后', self.next_painting, 'icons/next.png')

        self._ok_button = Button(app, self._surface, (13, 20 + 5 * button_step_y, 65, 35), '确定', self.ok, 'icons/confirm.png')

        self._cancel_button = Button(app, self._surface, (13, 20 + 6 * button_step_y, 65, 35), '取消', self.cancel, 'icons/back.png')

        self._rect = surface.get_rect()

    def show_paintings(self, folder, caller):
        self._folder = folder
        self._caller = caller
        self._painting_files = sorted(glob.glob('{}/*.png'.format(self._folder)))

        self._remove_all_buttons()

        if self._has_painting:
            self._current_painting_index = len(self._painting_files) - 1
            self._load_current_painting()
            self._buttons.append(self._previous_button)
            self._buttons.append(self._next_button)
            self._buttons.append(self._ok_button)
            self._buttons.append(self._cancel_button)
        else:
            self._buttons.append(self._cancel_button)

    def paint(self):
        pygame.draw.rect(self._surface, self._config.dialog_background_color,
                         (0, 0, self._config.win_width, self._config.win_height))

        if self._has_painting:
            self._surface.blit(self._current_painting,
                           (self._config._paint_pos_x, self._config._paint_pos_y,
                            self._config.paint_width, self._config.paint_height))
        else:
            text_surface = self._app.font.render('没有图像文件', True, self._config.button_text_color)
            text_rect = text_surface.get_rect()
            text_rect[0] = self._rect[0] + (self._rect[2] - text_rect[2]) // 2
            text_rect[1] = self._rect[1] + (self._rect[3] - text_rect[3]) // 3 + 25
            self._surface.blit(text_surface, text_rect)

        Dialog.paint(self)

    def _load_current_painting(self):
        self._current_painting =  pygame.image.load(self._painting_files[self._current_painting_index])

    def previous_painting(self):
        if self._current_painting_index > 0:
            self._current_painting_index -= 1
        self._load_current_painting()

    def next_painting(self):
        if self._current_painting_index < len(self._painting_files) - 1:
            self._current_painting_index += 1
        self._load_current_painting()

    def ok(self):
        self._caller.load(self._painting_files[self._current_painting_index])

    def cancel(self):
        self._caller.cancel()

    @property
    def _has_painting(self):
        return len(self._painting_files) > 0