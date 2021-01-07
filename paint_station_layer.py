
class Layer():
    def __init__(self, app, surface):
        self._app = app
        self._surface = surface
        self._buttons = []

    def paint(self):
        for button in self._buttons:
            button.paint()

    def mouse_down(self, pos):
        for button in self._buttons:
            if button.mouse_down(pos):
                return True
        return False

    def mouse_move(self, pos):
        for button in self._buttons:
            if button.mouse_move(pos):
                return True
        return False

    def mouse_up(self, pos):
        for button in self._buttons:
            if button.mouse_up(pos):
                return True
        return False

    def key_down(self, key):
        for button in self._buttons:
            if button.key_down(key):
                return True
        return False

    def _remove_all_buttons(self):
        self._buttons.clear()