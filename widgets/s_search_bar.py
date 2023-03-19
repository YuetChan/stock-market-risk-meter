from PyQt5.QtWidgets import QWidget, QLineEdit,QHBoxLayout

class s_file_search_bar(QWidget):

    def __init__(
            self, 
            parent=None
            ):
        super(s_file_search_bar, self).__init__(parent)

        self._init_ui()


    def connect_text_changed(self, l_func):
        self.search_line_edit.textChanged.connect(l_func)


    def _init_ui(self):
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(0)
        
        self.search_line_edit = QLineEdit(self)

        layout.addWidget(self.search_line_edit)

        self.search_line_edit.setPlaceholderText('Search...')
        
        self.setLayout(layout)

