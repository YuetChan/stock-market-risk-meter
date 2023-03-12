import Levenshtein

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QLineEdit,QHBoxLayout

class levenshtein_sort_proxy_model(QSortFilterProxyModel):
    
    def lessThan(
        self, 
        left_index, 
        right_index
        ):
        left_data = self.sourceModel().data(left_index)
        right_data = self.sourceModel().data(right_index)

        return Levenshtein.ratio(
            left_data, 
            self.filterRegExp().pattern()) < Levenshtein.ratio(
            right_data, 
            self.filterRegExp().pattern())
    

class s_file_search_bar(QWidget):

    def __init__(
        self, 
        parent=None
        ):
        super(s_file_search_bar, self).__init__(parent)
        
        # Create a layout to hold the line edit and label
        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 5)
        layout.setSpacing(0)
        
        # Create a line edit for the search text
        self.search_line_edit = QLineEdit(self)

        layout.addWidget(self.search_line_edit)

        self.search_line_edit.setPlaceholderText('Search...')


        # # Add a spacer item to create some space between the icon and the line edit
        # spacer_item = QSpacerItem(4, 1, QSizePolicy.Fixed, QSizePolicy.Fixed)

        # layout.addItem(spacer_item)

        # # Create a label for the file icon
        # ficon = QIcon.fromTheme('text-x-generic')

        # self.ficon_label = QLabel(self)

        # self.ficon_label.setPixmap(ficon.pixmap(16, 16))
        # self.ficon_label.setAlignment(Qt.AlignCenter)

        # layout.addWidget(self.ficon_label)


    def set_list_view(
        self, 
        list_view
        ):
        # Create an instance of the custom proxy model
        proxy_model = levenshtein_sort_proxy_model()

        proxy_model.setSourceModel(list_view.src_model)
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Set the proxy model as the model for the list widget
        list_view.setModel(proxy_model)
    
        self.list_view = list_view

        # Connect the search bar's text changed signal to update the filter regex pattern for the proxy model
        self.search_line_edit.textChanged.connect(lambda text: proxy_model.setFilterRegExp(text))

