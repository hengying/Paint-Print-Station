from paint_station_config import Config

class HistoryManager():
    def __init__(self):
        self._historys = []
        self._config = Config()
        self._max_undo_count = self._config.max_undo_count
        self._current_pos = -1

    def add_history(self, his):
        self._historys = self._historys[0:self._current_pos + 1]

        self._historys.append(his)
        self._current_pos += 1
        if len(self._historys) > self._max_undo_count:
            self._historys.pop(0)
            self._current_pos -= 1

    def undo(self):
        his = None
        if self._current_pos > 0:
            self._current_pos -= 1
            his = self._historys[self._current_pos]

        return his

    def redo(self):
        his = None
        if self._current_pos < len(self._historys) - 1:
            self._current_pos += 1
            his = self._historys[self._current_pos]

        return his