from config_reader import config_reader
import core_helper
from core_manager import core_manager
import db_connector
import fs_helper

from PyQt5 import QtGui


from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush

from widgets.s_file_tree import s_file_tree
from widgets.s_file_list import s_file_list
from widgets.s_main_window import s_main_window

if __name__ == '__main__':
    app = QApplication([])

    main_window = s_main_window()
    
    main_window.resize(1200, 900)
    main_window.show()

    app.exec_()
    
