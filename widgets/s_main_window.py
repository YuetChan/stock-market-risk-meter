import os
import uuid
import json

from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMenu, QSplitter, QVBoxLayout, QWidget, QLabel, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QIcon

from config_reader import config_reader

from core_helper import core_helper
from core_manager import core_manager
from db_connector import db_connector
from fs_helper import fs_helper

from widgets.s_file_search_bar import s_file_search_bar
from widgets.s_project_config_dialog import s_project_config_dialog
from widgets.s_text_edit_tool_bar import s_text_edit_tool_bar
from widgets.s_text_edit_area import s_text_edit_area
from widgets.s_file_tree import s_file_tree
from widgets.s_file_list import s_file_list

class s_main_window(QMainWindow):
    
    def __init__(
            self, 
            parent=None
            ):
        super(s_main_window, self).__init__(parent)
        
        self._init_dialogs_ui()
        self._init_actions_ui()
        
        self.left_panel = None
        self.right_panel = None

        self.central_splitter = None

        self.c_helper = core_helper(db_connector('./resources/test.db').get_connection())

        self.c_config = { }
        self.c_manager = None

        self.default_config_fname = 's_config.json'


    def new_project(self):
        # Clean up previous widgets
        self._clean_up()

        self.c_config['root_dir'] = QFileDialog().getExistingDirectory(            
            None,
            'Select a folder:',
            '',
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
            )

        if os.path.exists(os.path.join(self.c_config['root_dir'], self.default_config_fname)):
            self._show_config_file_existed_msg()
                
        else:
            if self._prompt_project_config():
                self._init_core_ui()

            else:
                self._show_config_file_create_failed_msg()
                

    def open_project(self):
        # Clean up previous widgets
        self._clean_up()

        self.c_config['root_dir'] = QFileDialog().getExistingDirectory(
            None,
            'Select a folder:',
            '',
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
        )

        if os.path.exists(os.path.join(self.c_config['root_dir'], self.default_config_fname)):
            c_reader = config_reader(self.default_config_fname)

            if c_reader.is_valid:
                self.c_config['project_id'] = c_reader.get_project_id()
                self.c_config['project_name'] = c_reader.get_project_name()
            
                self._init_core_ui()

            else:
                self._show_config_file_not_valid_msg()
  

        else:
            self._show_config_file_missing_msg()


    def _init_dialogs_ui(self):
        self.dialog = s_project_config_dialog()


    def _init_actions_ui(self):
        self.setWindowTitle('Sc Note')

        self._init_file_menu()

        self._init_new_project_action()
        self._init_open_project_action()

        self._init_auto_save_action()


    def _init_file_menu(self):
        self.file_menu = QMenu('File', self)

        self.menuBar().addMenu(self.file_menu)

    
    def _init_new_project_action(self):
        action = QAction('New Project', self)

        action.triggered.connect(self.new_project)
        self.file_menu.addAction(action)


    def _init_open_project_action(self):
        action = QAction('Open Project', self)

        action.triggered.connect(self.open_project)
        self.file_menu.addAction(action)


    def _init_auto_save_action(self):
        action = QAction('Auto Save', self)

        action.setCheckable(False)
        action.setIcon(QIcon('./resources/check-solid.svg'))

        self.file_menu.addAction(action)


    def _prompt_project_config(self):
        if self.dialog.exec_() == QDialog.Accepted:
            self.c_config['project_name'] = self.dialog.get_project_name()
            self.c_config['project_id'] = str(uuid.uuid4())

            try:    
                with open(os.path.join(self.c_config['root_dir'], self.default_config_fname), 'w') as f:
                    json.dump({
                        'id': self.c_config['project_id'],
                        'name': self.c_config['project_name']
                    }, f)

                return True

            except Exception as e:
                print("Error occurred while writing data to file:", e)
                return False


        else:
            print("Project config dialog rejected")
            return False
        

    def _init_core_ui(self):
        self._init_file_tree()
        self._init_file_list()

        self._init_text_edit()

        self._init_left_panel()
        self._init_right_panel()

        self.central_splitter = QSplitter()
    
        self.central_splitter.addWidget(self.left_panel)
        self.central_splitter.addWidget(self.right_panel)

        self.setCentralWidget(self.central_splitter)
        
        self.c_manager = core_manager(
            self.c_config['project_id'], 
            self.file_tree, 
            self.text_edit_area_label, 
            self.text_edit_area, 
            self.text_edit_tool_bar, 
            self.c_helper
            )


    def _init_file_tree(self):
        all_fpaths = fs_helper.get_all_filepaths(self.c_config['root_dir'])

        fpath_rows = self.c_helper.select_filepaths_with_non_empty_plain_text_note_by_project_id_n_filepaths_in(
            self.c_config['project_id'], 
            all_fpaths
            )
        
        hl_fpaths = []

        for row in fpath_rows:
            hl_fpaths.append(row[0])


        hl_decorator = lambda item: item.setForeground(QBrush(QColor('green')))

        self.file_tree = s_file_tree(
            self.c_config['project_name'], 
            self.c_config['root_dir'], 
            hl_fpaths,
            hl_decorator)
    
        self.file_tree.setMaximumWidth(300)


    def _init_file_list(self):
        list_model = QStandardItemModel()

        item1 = QStandardItem('Item 1')
        item2 = QStandardItem('Item 2')
        item3 = QStandardItem('Item 3')

        list_model.appendRow(item1)
        list_model.appendRow(item2)
        list_model.appendRow(item3)

        self.file_list =  s_file_list(list_model)

        self.search_bar_title = QLabel('Dangling Notes')

        self.search_bar = s_file_search_bar(self)

        self.search_bar.set_file_list(self.file_list)


    def _init_text_edit(self):
        self.text_edit_area_label = QLabel('')

        self.text_edit_area = s_text_edit_area()

        self.text_edit_tool_bar = s_text_edit_tool_bar(self.text_edit_area)


    def _init_left_panel(self):
        v_box = QVBoxLayout()

        v_box.addWidget(self.search_bar_title)
        v_box.addWidget(self.search_bar)

        v_box.addWidget(self.file_list)

        file_list_widget = QWidget()

        file_list_widget.setLayout(v_box)

        self.left_panel = QSplitter()

        self.left_panel.addWidget(self.file_tree)
        self.left_panel.addWidget(file_list_widget)

        self.left_panel.setOrientation(Qt.Vertical)  
        self.left_panel.setSizes([600, 300])


    def _init_right_panel(self):
        v_box = QVBoxLayout()

        v_box.addWidget(self.text_edit_area_label)

        v_box.addWidget(self.text_edit_tool_bar)
        v_box.addWidget(self.text_edit_area)

        self.right_panel = QWidget()

        self.right_panel.setLayout(v_box)
    

    def _show_config_file_existed_msg(self):
        QMessageBox.critical(
            None, 
            'Error', 
            'The selected directory already contain a configuration file.'
            )


    def _show_config_file_create_failed_msg(self):
        QMessageBox.critical(
            None, 
            'Error', 
            'Failed to create a configuration file.'
            )


    def _show_config_file_missing_msg(self):
        QMessageBox.critical(
            None, 
            'Error', 
            'The selected directory does not contain a configuration file.'
            )
        
    
    def _show_config_file_not_valid_msg(self):
        QMessageBox.critical(
            None, 
            'Error', 
            'The selected directory does not contain a valid configuration.'
            )
        

    def _clean_up(self):
        # Central splitter contains all widgets. 
        # Deleting central splitter would delete all widgets
        if self.central_splitter != None:
            self.central_splitter.deleteLater()

            # deleteLater() doesnt remove the reference. 
            # This removes reference manually
            self.central_splitter = None

            