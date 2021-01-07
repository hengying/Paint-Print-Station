import time
import threading
import configparser


class SingletonType(type):
    _instance_lock = threading.Lock()
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance

class Config(metaclass=SingletonType):
    def __init__(self):
        self.__config = configparser.ConfigParser()
        self.__config_file = "paint_station_config.ini"
        self.__config.read(self.__config_file)

        if self.__config.has_option('win', 'win_pos_x'):
            self._win_pos_x = int(self.__config.get('win', 'win_pos_x'))
        else:
            self._win_pos_x = None

        if self.__config.has_option('win', 'win_pos_y'):
            self._win_pos_y = int(self.__config.get('win', 'win_pos_y'))
        else:
            self._win_pos_y = None

        if self.__config.has_option('win', 'display_english'):
            self._display_english = int(self.__config.get('win', 'display_english'))
        else:
            self._display_english = 0

        if self.__config.has_option('win', 'current_brush_index'):
            self._saved_current_brush_index = int(self.__config.get('win', 'current_brush_index'))
        else:
            self._saved_current_brush_index = 0

        if self.__config.has_option('image', 'use_escpos'):
            self._use_escpos = int(self.__config.get('image', 'use_escpos'))
        else:
            self._use_escpos = 0

        if self.__config.has_option('image', 'print_command'):
            self._print_command = self.__config.get('image', 'print_command')
        else:
            self._print_command = None

        if self.__config.has_option('image', 'print_info_command'):
            self._print_info_command = self.__config.get('image', 'print_info_command')
        else:
            self._print_info_command = None

        self._win_width = 480
        self._win_height = 320

        self._paint_width = 384
        self._paint_height = 310

        self._max_undo_count = 21

        self._paint_pos_x = self._win_width - self._paint_width - 5
        self._paint_pos_y = (self._win_height - self._paint_height) // 2

        self._image_folder = self.__config.get('image', 'folder')
        self._show_cursor = int(self.__config.get('win', 'show_cursor')) == 1


    @property
    def win_pos_x(self):
        return self._win_pos_x

    @property
    def win_pos_y(self):
        return self._win_pos_y

    @property
    def win_width(self):
        return self._win_width

    @property
    def win_height(self):
        return self._win_height

    @property
    def paint_width(self):
        return self._paint_width

    @property
    def paint_height(self):
        return self._paint_height

    @property
    def paint_pos_x(self):
        return self._paint_pos_x

    @property
    def paint_pos_y(self):
        return self._paint_pos_y

    @property
    def display_english(self):
        return self._display_english

    @property
    def max_undo_count(self):
        return self._max_undo_count

    @property
    def image_folder(self):
        return self._image_folder

    @property
    def show_cursor(self):
        return self._show_cursor

    @property
    def saved_current_brush_index(self):
        return self._saved_current_brush_index

    @saved_current_brush_index.setter
    def saved_current_brush_index(self, value):
        self._saved_current_brush_index = value
        self.__config.set('win', 'current_brush_index', str(value))

    def save_config_file(self):
        self.__config.write(open(self.__config_file, "w"))

    @property
    def dialog_background_color(self):
        #return (125, 125, 125)
        return (40, 64, 125)

    @property
    def gui_background_color(self):
        #return (125, 125, 125)
        return (40, 64, 125)

    @property
    def brush_palette_grid_color(self):
        return (0, 125, 0)

    @property
    def highlight_color(self):
        return (255, 0, 0)

    @property
    def brush_editor_editable_grid_color(self):
        return (125, 125, 125)

    @property
    def brush_editor_not_editable_grid_color(self):
        return (0, 255, 0)

    @property
    def test_canvas_border_color(self):
        return (0, 255, 0)

    @property
    def button_background_color(self):
        return (0, 0, 0)

    @property
    def button_mouseover_color(self):
        return (50, 64, 50)

    @property
    def button_mousedown_color(self):
        return (90, 100, 90)

    @property
    def button_mousedown_mouseover_color(self):
        return (100, 125, 100)

    @property
    def button_border_color(self):
        return (100, 125, 100)

    @property
    def button_checked_border_color(self):
        return (255, 0, 0)

    @property
    def button_text_color(self):
        return (255, 255, 255)

    @property
    def canvas_init_color(self):
        return (255, 255, 255)

    @property
    def use_escpos(self):
        return self._use_escpos == 1

    @property
    def could_print(self):
        return self.use_escpos or self._print_command is not None

    def get_print_command(self, file_name):
        print_command = self._print_command
        if print_command.find('__filename__') != -1:
            print_command = print_command.replace('__filename__', '"{}"'.format(file_name))
        else:
            print_command = '{} "{}"'.format(print_command, file_name)

        return print_command

    def get_print_info_command(self):
        print_info_command = self._print_info_command
        if print_info_command is not None:
            print_info_command = print_info_command.replace('__datetime__', '"{}"'.format(self.get_print_time_str()))
        return print_info_command

    def get_print_time_str(self):
        return time.strftime('%y-%m-%d %H:%M:%S')