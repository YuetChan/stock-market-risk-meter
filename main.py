from config_reader import config_reader
import core_helper
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

    creader = config_reader('s_config.json')

    app = QApplication([])

    all_fpaths = fs_helper.get_all_filepaths('./')
    config_fpaths = creader.get_all_filepaths()

    matched_result = fs_helper.find_matched_filepaths(all_fpaths, config_fpaths)

    dangling_fpaths = matched_result['dangling_fpaths']

    hl_fpaths = matched_result['matched_fpaths']
    hl_decorator = lambda item: item.setForeground(QBrush(QColor('green')))

    tree_widget = s_file_tree(
        'id', 
        'project_1', 
        './', 
        all_fpaths, 
        hl_fpaths,
        hl_decorator)
    
    tree_widget.setMaximumWidth(300)
    
    list_model = QStandardItemModel()

    item1 = QStandardItem("Item 1")
    item2 = QStandardItem("Item 2")
    item3 = QStandardItem("Item 3")

    list_model.appendRow(item1)
    list_model.appendRow(item2)
    list_model.appendRow(item3)

    list_view = s_file_list(list_model)

    main_window = s_main_window(tree_widget, list_view)
    
    main_window.resize(1200, 900)
    main_window.show()
    # tree.decorate_item()
    # print(tree.find_by_fname('.git'))
    # tree.print_tree()

    # print(tree.find_by_fname('.git'))
    # tree.show()

    app.exec_()
    
