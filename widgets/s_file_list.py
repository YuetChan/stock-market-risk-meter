from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListView

class s_file_list(QListView):

    file_clicked = pyqtSignal(dict)

    def __init__(
            self, 
            model,
            parent=None
            ):
        super(s_file_list, self).__init__(parent)

        self.src_model = model
        self.setModel(model)

        self.selected_fpath = None

        self.clicked.connect(self._on_file_clicked)


    def _on_file_clicked(self, idx):
        self.selected_fpath = self.model().data(idx)

        self.file_clicked.emit({
            'file_path': self.selected_fpath,
        })

