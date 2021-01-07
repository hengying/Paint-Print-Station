from paint_station_layer import Layer

class Dialog(Layer):
    def __init__(self, app, surface):
        Layer.__init__(self, app, surface)

    def mouse_down(self, pos):
        if Layer.mouse_down(self, pos):
            return True

        # return True because dialog is modal
        return True

    def mouse_move(self, pos):
        if Layer.mouse_move(self, pos):
            return True

        # return True because dialog is modal
        return True

    def mouse_up(self, pos):
        if Layer.mouse_up(self, pos):
            return True

        # return True because dialog is modal
        return True

    def key_down(self, key):
        if Layer.key_down(self, key):
            return True

        # return True because dialog is modal
        return True
