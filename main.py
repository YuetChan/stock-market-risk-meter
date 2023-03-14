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
    # db_connector.init('test.db')
    # db_proxy.init_project('test_project_1')
    
    # db_proxy.select_project_by_id("3412cf74-8d46-40c1-9f88-0e6a1ae7cbbc")

    # db_proxy.add_note_by_file_path_n_projectid("note1", "./test", "3412cf74-8d46-40c1-9f88-0e6a1ae7cbbc")

    # db_proxy.update_note_by_file_path_n_projectid("note_1_c", "./test", "3412cf74-8d46-40c1-9f88-0e6a1ae7cbbc")
    # db_proxy.select_notes_by_filepath_like_n_project_id("./test%", "3412cf74-8d46-40c1-9f88-0e6a1ae7cbbc")
    
    # db_connector.close()

    # print(config_reader.get_all_filepaths())

    creader = config_reader('./s_config.json')

    app = QApplication([])

    main_window = s_main_window()
    
    main_window.resize(1200, 900)
    main_window.show()
    # tree.decorate_item()
    # print(tree.find_by_fname('.git'))
    # tree.print_tree()

    # print(tree.find_by_fname('.git'))
    # tree.show()

    app.exec_()
    
