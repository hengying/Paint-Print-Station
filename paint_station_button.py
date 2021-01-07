import pygame
from paint_station_config import Config

BLACK = (0, 0, 0)

class Button():
    def __init__(self, app, surface, rect, text, call_back, icon_file = None):
        self.__app = app
        self.__surface = surface
        self._config = Config()
        self._rect = rect
        self._text = text
        self._icon_file = icon_file
        self._call_back = call_back
        self._mouse_down = False
        self._mouse_over = False
        self._is_checked = False
        if self._icon_file is not None:
            self._icon = pygame.image.load(icon_file)
            self._icon.set_colorkey(BLACK)

    def paint(self):
        background_color = (0, 0, 0)
        if self._mouse_over:
            if self._mouse_down:
                background_color = self._config.button_mousedown_mouseover_color
            else:
                background_color = self._config.button_mouseover_color
        else:
            if self._mouse_down:
                background_color = self._config.button_mousedown_color
            else:
                background_color = self._config.button_background_color

        pygame.draw.rect(self.__surface, background_color, self._rect)

        pygame.draw.rect(self.__surface,
                         self._config.button_checked_border_color if self._is_checked else self._config.button_border_color,
                         self._rect, width=1)

        if self._icon_file is not None:
            icon_rect = self._icon.get_rect()
            icon_rect[0] = self._rect[0] + (self._rect[2] - icon_rect[2]) // 2
            icon_rect[1] = self._rect[1] + (self._rect[3] - icon_rect[3]) // 2
            self.__surface.blit(self._icon, icon_rect)
        else:
            text_surface = self.__app.font.render(self._text, True, self._config.button_text_color)
            text_rect = text_surface.get_rect()
            text_rect[0] = self._rect[0] + (self._rect[2] - text_rect[2]) // 2
            text_rect[1] = self._rect[1] + (self._rect[3] - text_rect[3]) // 2
            self.__surface.blit(text_surface, text_rect)

    def mouse_down(self, pos):
        if pos[0] >= self._rect[0] \
            and pos[0] < self._rect[0] + self._rect[2] \
            and pos[1] >= self._rect[1] \
            and pos[1] < self._rect[1] + self._rect[3]:
                self._mouse_down = True
                return True
        else:
            return False

    def mouse_move(self, pos):
        if pos[0] >= self._rect[0] \
                and pos[0] < self._rect[0] + self._rect[2] \
                and pos[1] >= self._rect[1] \
                and pos[1] < self._rect[1] + self._rect[3]:
            self._mouse_over = True
        else:
            self._mouse_over = False

        if self._mouse_down:
            return True

        return False

    def mouse_up(self, pos):
        if self._mouse_down:
            if pos[0] >= self._rect[0] \
                    and pos[0] < self._rect[0] + self._rect[2] \
                    and pos[1] >= self._rect[1] \
                    and pos[1] < self._rect[1] + self._rect[3]:
                self._call_back()
            self._mouse_down = False
            self._mouse_over = False
            return True

        return False

    def key_down(self, key):
        return False

    @property
    def is_checked(self):
        return self._is_checked

    @is_checked.setter
    def is_checked(self, value):
        self._is_checked = value
