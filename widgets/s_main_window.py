import os
import uuid
import json

from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMenu, QSplitter, QLabel, QMessageBox, QDialog
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QIcon

from config_reader import config_reader

from core_helper import core_helper
from core_manager import core_manager
from fs_helper import fs_helper

from widgets.s_single_input_dialog import s_single_input_dialog
from widgets.s_search_bar import s_file_search_bar
from widgets.s_rich_text_editor.s_rich_text_editor import s_rich_text_editor
from widgets.s_file_tree import s_file_tree
from widgets.s_file_list import s_file_list

from widgets.s_file_searcher.s_file_searcher import s_file_searcher

class s_main_window(QMainWindow):
    
    def __init__(
            self, 
            parent=None
            ):
        super(s_main_window, self).__init__(parent)
        
        self._init_dialogs_ui()
        self._init_actions_ui()
        
        self.hl_fpath = []
        self.dangling_fpath = []

        self.left_panel = None
        self.right_panel = None

        self.central_splitter = None

        self.file_tree = None
        self.text_editor = None

        self.c_helper = None

        self.c_config = { }
        self.c_manager = None

        self.default_config_fname = 's_config.json'


    def new_project(self):
        self.c_config['root_dir'] = QFileDialog().getExistingDirectory(            
            None,
            'Select a folder:',
            '',
            QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
            )

        if self.c_config['root_dir'] == '':
            return
        

        if os.path.exists(os.path.join(self.c_config['root_dir'], self.default_config_fname)):
            self._show_config_file_existed_msg()
                
        elif self._prompt_project_config():
            c_reader = config_reader(os.path.join(self.c_config['root_dir'], self.default_config_fname))
            self.c_helper = core_helper(c_reader)

             # Clean up previous widgets before init new widgets
            self._clean_up()
            self._init_core_ui()

        else:
            self._show_config_file_create_failed_msg()
                

    def open_project(self):
        fpath = QFileDialog().getOpenFileName(
            None, 
            "Open s_config.json", 
            "", 
            "JSON Files (*.json);;All Files (*)", 
            options= QFileDialog.Options() | QFileDialog.DontUseNativeDialog
            )[0]
        
        if fpath == '':
            return
            

        if  os.path.basename(fpath) == self.default_config_fname:
            c_reader = config_reader(fpath)

            self.c_helper = core_helper(c_reader)

            if c_reader.is_valid:
                self.c_config['project_id'] = c_reader.get_project_id()
                self.c_config['project_name'] = c_reader.get_project_name()

                self.c_config['user'] = c_reader.get_user()
                self.c_config['root_dir'] = os.path.dirname(fpath)
                
                self._clean_up()
                self._init_core_ui()

            else:
                self._show_config_file_not_valid_msg()
  

        else:
            self._show_config_file_missing_msg()


    def _init_dialogs_ui(self):
        self.dialog = s_single_input_dialog({
            'dialog_title': 'New Project',
            'dialog_var_1': 'project_name',
            'dialog_var_2': 'user',
            'dialog_var_3': 'dirpath',
            'dialog_msg_1': 'Enter a project name',
            'dialog_msg_2': 'Enter an username',
            'dialog_msg_3': 'Choose a datasource directory',
        })


    def _init_actions_ui(self):
        self.setWindowTitle('Code Meta')

        self._init_file_menu()

        self._init_new_project_action()
        self._init_open_project_action()

        self._init_auto_save_action()


    def _init_file_menu(self):
        self.file_menu = QMenu('File', self)

        self.menuBar().addMenu(self.file_menu)

    
    def _init_new_project_action(self):
        action = QAction(
            'New Project', 
            self
            )

        action.triggered.connect(self.new_project)
        self.file_menu.addAction(action)


    def _init_open_project_action(self):
        action = QAction(
            'Open Project', 
            self
            )

        action.triggered.connect(self.open_project)
        self.file_menu.addAction(action)


    def _init_auto_save_action(self):
        action = QAction(
            QIcon(os.environ['code_meta_dir'] + '/resources/check-solid.svg'), 
            'Auto Save', 
            self
            )

        action.setCheckable(False)
        self.file_menu.addAction(action)


    def _prompt_project_config(self):
        if self.dialog.exec_() == QDialog.Accepted:
            self.c_config['project_id'] = str(uuid.uuid4())
            self.c_config['project_name'] = self.dialog.get_config()['project_name']
            self.c_config['user'] = self.dialog.get_config()['user']         

            try:
                self.init_config(
                    self.c_config['project_id'], 
                    self.c_config['project_name'], 
                    self.c_config['user'],
                    os.path.join(self.c_config['root_dir'], self.default_config_fname)
                    )    

                return True

            except Exception as e:
                print("Error occurred while writing data to file:", e)
                return False


        else:
            print("Project input dialog rejected")
            return False
        

    def _init_core_ui(self):
        self._init_left_panel()
        self._init_right_panel()

        self._init_central_widget()

        self.c_manager = core_manager(
            self.c_config['project_id'], 
            self.file_tree, 
            self.file_searcher,
            self.text_editor,
            self.c_helper
            )


    def _init_file_tree(self):
        print(self.c_config['root_dir'])

        all_fpaths = fs_helper.relativize_file_paths(
            fs_helper.get_all_filepaths(self.c_config['root_dir'])
            )

        hl_fpaths = self.c_helper.select_filepaths_with_non_empty_plain_text_note_by_filepaths_in(all_fpaths)
        
        hl_decorator = lambda item: item.setForeground(QBrush(QColor('green')))

        self.file_tree = s_file_tree(
            fs_helper.relativize_file_paths(hl_fpaths),
            hl_decorator
            )

        self.file_tree.setModel(
            self._populate_file_tree_model(self.c_config['root_dir'], self.c_config['project_name'])
            )
        self.file_tree.setMaximumWidth(300)


    def _init_file_searcher(self):
        all_fpaths = fs_helper.relativize_file_paths(
            fs_helper.get_all_filepaths(self.c_config['root_dir'])
            )

        fpaths = self.c_helper.select_filepaths_with_non_empty_plain_text_note_by_filepaths_not_in(all_fpaths)

        model = QStandardItemModel()

        for fpath in fpaths:
            item = QStandardItem(fpath)

            model.appendRow(item)


        self.search_title = QLabel('Dangling Notes')

        self.search_bar = s_file_search_bar()

        self.file_list = s_file_list(model)

        self.file_searcher = s_file_searcher(self.search_title, self.search_bar, self.file_list)


    def _init_left_panel(self):
        self._init_file_tree()
        self._init_file_searcher()
    
        self.left_panel = QSplitter()

        self.left_panel.addWidget(self.file_tree)
        self.left_panel.addWidget(self.file_searcher)

        self.left_panel.setOrientation(Qt.Vertical)  
        self.left_panel.setSizes([600, 300])
    

    def _init_right_panel(self):
        self.text_editor = s_rich_text_editor()
        self.right_panel = self.text_editor


    def _init_central_widget(self):
        self.central_splitter = QSplitter()

        self.central_splitter.addWidget(self.left_panel)
        self.central_splitter.addWidget(self.right_panel)

        self.setCentralWidget(self.central_splitter)
        

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
        if self.central_splitter != None:
            self.central_splitter.deleteLater()

            # deleteLater() doesnt remove the reference  
            # and this removes reference manually
            self.central_splitter = None

            
    def _populate_file_tree_model(
            self, 
            root_dir,
            label
            ):
        # Special case
        root_item = QStandardItem('.')

        root_item.setData(QVariant([fs_helper.relativize_file_path(root_dir), True]), Qt.UserRole)

        model = QStandardItemModel()

        model.setHorizontalHeaderLabels([label])
        model.appendRow(root_item)

        self._add_files(root_item, root_dir)

        return model


    def _add_files(
            self, 
            parent, 
            path,
            
            ):
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)

            if not os.path.isdir(fpath):
                item = QStandardItem(fname)
                
                item.setData(QVariant([fs_helper.relativize_file_path(fpath), False]), Qt.UserRole)
                parent.appendRow(item)


            if os.path.isdir(fpath):
                item = QStandardItem(fname)

                item.setData(QVariant([fs_helper.relativize_file_path(fpath), True]), Qt.UserRole)
                parent.appendRow(item)

                self._add_files(item, fpath)


    def init_config(
            self,
            id, 
            name, 
            user,
            fpath):
        json_data = {
          "id": id,
          "name": name,
          "user": user,
          "file_paths": { }
        }

        with open(fpath, 'w') as outfile:
            json.dump(json_data, outfile)


