from config_reader import config_reader
from core_manager import core_manager

from PyQt5.QtWidgets import QApplication

from widgets.s_main_window import s_main_window

if __name__ == '__main__':
    app = QApplication([])

    main_window = s_main_window()
    
    main_window.resize(1200, 900)
    main_window.show()

    app.exec_()
    
