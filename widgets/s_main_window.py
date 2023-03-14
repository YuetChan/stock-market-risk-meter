from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMenu, QSplitter, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor, QIcon

from config_reader import config_reader

from core_helper import core_helper
from core_manager import core_manager
from db_connector import db_connector
from fs_helper import fs_helper

from widgets.s_file_search_bar import s_file_search_bar
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
        
        self.init_ui()

        db = db_connector('./resources/test.db')
        self.db_conn = db.getConnection()
        
        self.setWindowTitle("Sc Note")




    def init_ui(self):
        fileMenu = QMenu('File', self)

        self.menuBar().addMenu(fileMenu)

        newAction = QAction('New Project', self)

        newAction.triggered.connect(self.create_new_project)

        fileMenu.addAction(newAction)

        openAction = QAction('Open Project', self)

        openAction.triggered.connect(self.open_project)

        fileMenu.addAction(openAction)

        auto_save_action = QAction('Auto Save', self)

        auto_save_action.setCheckable(False)
        auto_save_action.setIcon(QIcon('./resources/check-solid.svg'))

        fileMenu.addAction(auto_save_action)
        
        # closeAction = QAction('Close Project', self)
    
        # closeAction.setDisabled(True)
        # closeAction.triggered.connect(self.close_project)
        
        # fileMenu.addAction(closeAction)


    def init_left_panel():
        return
    

    def init_right_panel():
        return


    def create_new_project(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if dir_path:
        # Create new project in directory
        # ...
        # Enable the close action
            self.close_action.setEnabled(True)


    def open_project(self):
        # root_dir = QFileDialog.getExistingDirectory(
        #     None,
        #     "Select a folder:",
        #     "",
        #     QFileDialog.ShowDirsOnly
        # )

        # print(root_dir)


        # c_helper = core_helper(db_conn)

        # c_reader = config_reader('s_config.json')

        # project_id = c_reader.get_project_id()
        # all_fpaths = fs_helper.get_all_filepaths(root_dir)
       
        # hl_fpaths = c_helper.select_filepaths_with_non_empty_note_by_project_id_n_filepaths_in(project_id, all_fpaths)
        # hl_decorator = lambda item: item.setForeground(QBrush(QColor('green')))

        # file_tree = s_file_tree(
        #     project_id, 
        #     'project_1', 
        #     root_dir, 
        #     hl_fpaths,
        #     hl_decorator)
    
        # file_tree.setMaximumWidth(300)

        # self.file_tree = file_tree

        # list_model = QStandardItemModel()

        # item1 = QStandardItem("Item 1")
        # item2 = QStandardItem("Item 2")
        # item3 = QStandardItem("Item 3")

        # list_model.appendRow(item1)
        # list_model.appendRow(item2)
        # list_model.appendRow(item3)

        # file_list = s_file_list(list_model)

        # self.file_list = file_list

        # search_bar_widget = s_file_search_bar(self)

        # search_bar_widget.set_file_list(file_list)

        # self.text_edit_area_label = QLabel('')

        # self.text_edit_area = s_text_edit_area()

        # self.text_edit_tool_bar = s_text_edit_tool_bar(self.text_edit_area)

        # self.text_edit_tool_bar.set_main_window(self)

        # # Create a label for the title
        # search_bar_title = QLabel("Dangling Notes")

        # # Create layout for search bar and list widget
        # vbox1 = QVBoxLayout()

        # vbox1.addWidget(search_bar_title)
        # vbox1.addWidget(search_bar_widget)
        # vbox1.addWidget(file_list)

        # # Create widget to hold search bar and list widget
        # left_panel_widget = QWidget()

        # left_panel_widget.setLayout(vbox1)

        # # Create splitter
        # splitter1 = QSplitter()

        # splitter1.addWidget(self.file_tree)
        # splitter1.addWidget(left_panel_widget)

        # # Vertical splitter
        # splitter1.setOrientation(Qt.Vertical)  
        # splitter1.setSizes([600, 300])
        
        # # Create layout for tool bar and text edit area
        # vbox2 = QVBoxLayout()

        # vbox2.addWidget(self.text_edit_area_label)
        # vbox2.addWidget(self.text_edit_tool_bar)
        # vbox2.addWidget(self.text_edit_area)

        # # Create widget to hold search bar and list widget
        # right_panel_widget = QWidget()

        # right_panel_widget.setLayout(vbox2)

        # # Create another splitter for left and right sides
        # splitter2 = QSplitter()
    
        # splitter2.addWidget(splitter1)
        # splitter2.addWidget(right_panel_widget)
    
        # # Set the main window widget
        # self.setCentralWidget(splitter2)
        # self.setWindowTitle("Sc Note")

        
        # c_manager = core_manager(
        #     'id', 
        #     self.file_tree, 
        #     self.text_edit_area_label, 
        #     self.text_edit_area, 
        #     self.text_edit_tool_bar, 
        #     c_helper
        #     )

        # Code to open an existing project
        pass


    def close_project(self):
        # Code to close the current project
        pass