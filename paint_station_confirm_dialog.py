import pygame
from paint_station_dialog import Dialog
from paint_station_config import Config
from paint_station_button import Button

class ConfirmDialog(Dialog):
    def __init__(self, app, surface):
        Dialog.__init__(self, app, surface)
        self._config = Config()

        self._ok_button = Button(app, self._surface, (260, 212, 65, 35), '确定', self.ok, 'icons/confirm.png')
        self._buttons.append(self._ok_button)

        self._cancel_button = Button(app, self._surface, (158, 212, 65, 35), '取消', self.cancel, 'icons/back.png')
        self._buttons.append(self._cancel_button)

        self._rect = surface.get_rect()

    def show_confirm_dialog(self, text, caller):
        self._text = text
        self._caller = caller

    def paint(self):
        pygame.draw.rect(self._surface, self._config.dialog_background_color,
                         (0, 0, self._config.win_width, self._config.win_height))

        text_surface = self._app.font.render(self._text, True, self._config.button_text_color)
        text_rect = text_surface.get_rect()
        text_rect[0] = self._rect[0] + (self._rect[2] - text_rect[2]) // 2
        text_rect[1] = self._rect[1] + (self._rect[3] - text_rect[3]) // 3
        self._surface.blit(text_surface, text_rect)

        Dialog.paint(self)

    def ok(self):
        self._caller.ok()

    def cancel(self):
        self._caller.cancel()
