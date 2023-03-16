import Levenshtein

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QLineEdit,QHBoxLayout

class levenshtein_sort_proxy_model(QSortFilterProxyModel):
    
    def lessThan(
            self, 
            left_index, 
            right_index
            ):
        return Levenshtein.ratio(
            self.sourceModel().data(left_index), 
            self.filterRegExp().pattern()) < Levenshtein.ratio(
            self.sourceModel().data(right_index), 
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


    def set_file_list(
            self, 
            file_list
            ):
        # Create an instance of the custom proxy model
        proxy_model = levenshtein_sort_proxy_model()

        proxy_model.setSourceModel(file_list.src_model)
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        # Set the proxy model as the model for the list widget
        file_list.setModel(proxy_model)
    
        self.file_list = file_list

        # Connect the search bar's text changed signal to update the filter regex pattern for the proxy model
        self.search_line_edit.textChanged.connect(lambda text: proxy_model.setFilterRegExp(text))

