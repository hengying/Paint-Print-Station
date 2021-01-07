import os
from paint_station_config import Config

class Print():
    def __init__(self):
        self._config = Config()
        if self._config.use_escpos:
            self._init_printer()

    def _init_printer(self):
        try:
            # method 1
            '''
            create the escpos config file at:
            $HOME/.config/python-escpos/config.yaml
            
            printer:
                    type: Usb
                    idVendor: 0x0fe6
                    idProduct: 0x811e
                    in_ep: 0x82
                    out_ep: 0x02
            '''
            from escpos import config
            self._escpos_config = config.Config()
            self._printer = self._escpos_config.printer()

            # method 2
            '''
            from escpos.printer import Usb
            self._printer = Usb(0x0fe6, 0x811e, in_ep=0x82, out_ep=0x02)
            '''

        except ImportError:
            self._printer = None
            pass

    def print_image(self, image_file_name):
        if self._config.use_escpos:
            self._printer.image(image_file_name)
            self._printer.text(self._config.get_print_time_str() + '\n\n\n\n')
        else:
            print_command = self._config.get_print_command(image_file_name)
            print(print_command)
            os.system(print_command)

            print_info_command = self._config.get_print_info_command()
            if print_info_command is not None:
                print(print_info_command)
                os.system(print_info_command)
