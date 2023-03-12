from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMenu, QSplitter, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import Qt

from widgets.s_file_search_bar import s_file_search_bar
from widgets.s_text_edit_tool_bar import s_text_edit_tool_bar
from widgets.s_text_edit_area import s_text_edit_area

class s_main_window(QMainWindow):
    
    def __init__(
        self, 
        tree_widget, 
        list_view, 
        parent=None
        ):
        super(s_main_window, self).__init__(parent)

        self.tree_widget = tree_widget
        self.list_view = list_view

        search_bar_widget = s_file_search_bar(self)

        search_bar_widget.set_list_view(list_view)

        self.text_edit_area = s_text_edit_area()

        self.text_edit_tool_bar = s_text_edit_tool_bar(self.text_edit_area)

        self.text_edit_tool_bar.set_main_window(self)

        # Create a label for the title
        search_bar_title = QLabel("Dangling Notes")

        # Create layout for search bar and list widget
        vbox1 = QVBoxLayout()

        vbox1.addWidget(search_bar_title)
        vbox1.addWidget(search_bar_widget)
        vbox1.addWidget(list_view)

        # Create widget to hold search bar and list widget
        left_panel_widget = QWidget()

        left_panel_widget.setLayout(vbox1)

        # Create splitter
        splitter1 = QSplitter()

        splitter1.addWidget(self.tree_widget)
        splitter1.addWidget(left_panel_widget)

        # Vertical splitter
        splitter1.setOrientation(Qt.Vertical)  
        splitter1.setSizes([600, 300])
        
        # Create layout for tool bar and text edit area
        vbox2 = QVBoxLayout()

        vbox2.addWidget(QLabel("text edit"))
        vbox2.addWidget(self.text_edit_tool_bar)
        vbox2.addWidget(self.text_edit_area)

        # Create widget to hold search bar and list widget
        right_panel_widget = QWidget()

        right_panel_widget.setLayout(vbox2)

        # Create another splitter for left and right sides
        splitter2 = QSplitter()
    
        splitter2.addWidget(splitter1)
        splitter2.addWidget(right_panel_widget)
    
        # Set the main window widget
        self.setCentralWidget(splitter2)
        self.setWindowTitle("Sc Note")

        self.init_ui()


    def init_ui(self):
        fileMenu = QMenu('File', self)

        self.menuBar().addMenu(fileMenu)

        newAction = QAction('New Project', self)

        newAction.triggered.connect(self.create_new_project)

        fileMenu.addAction(newAction)

        openAction = QAction('Open Project', self)

        openAction.triggered.connect(self.open_project)

        fileMenu.addAction(openAction)

        closeAction = QAction('Close Project', self)
    
        closeAction.setDisabled(True)
        closeAction.triggered.connect(self.close_project)

        fileMenu.addAction(closeAction)


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
        # Code to open an existing project
        pass


    def close_project(self):
        # Code to close the current project
        pass