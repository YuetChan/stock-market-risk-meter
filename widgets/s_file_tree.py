import os

from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor

class s_file_tree(QTreeView):

    file_clicked = pyqtSignal(dict)

    def __init__(
            self, 
            label, 
            root_dir, 
            hl_fpaths,
            hl_decorator,
            parent=None
            ):
        super(s_file_tree, self).__init__(parent)

        self.selected_fpath = None

        self.is_dir_selected = None

        self.selected_item = None

        self.root_dir = root_dir

        self.hl_fpaths = hl_fpaths
        self.hl_decorator = hl_decorator

        self.setModel(self._populate(self.root_dir, label))
        self.expand(self.model().index(0, 0))

        self.default_decorator = lambda item: item.setForeground(QBrush(QColor('black')))
        
        self.clicked.connect(self._on_file_clicked)


    def decorate_selected_file(self):
         self._decorate_item(self.selected_item)


    def undecorate_selected_file(self):
        self._undecorate_item(self.selected_item)


    def _decorate_item(
            self, 
            item
            ):
        self.hl_decorator(item)


    def _undecorate_item(
            self,
            item
            ):
        self.default_decorator(item)
        

    def _populate(
            self, 
            root_dir,
            label
            ):
        root_item = QStandardItem(root_dir)

        root_item.setData(QVariant([root_dir, True]), Qt.UserRole)

        model = QStandardItemModel()

        model.setHorizontalHeaderLabels([label])
        model.appendRow(root_item)

        self._add_files(root_item, root_dir, model)

        return model


    def _add_files(
            self, 
            parent, 
            path,
            model
            ):
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)

            if not os.path.isdir(fpath):
                item = QStandardItem(fname)
                
                item.setData(QVariant([fpath, False]), Qt.UserRole)

                if fpath in self.hl_fpaths:
                    self._decorate_item(item)


                parent.appendRow(item)


            if os.path.isdir(fpath):
                item = QStandardItem(fname)

                item.setData(QVariant([fpath, True]), Qt.UserRole)
                parent.appendRow(item)

                self._add_files(item, fpath, model)


    def _on_file_clicked(
            self, 
            index
            ):
        self.selected_item = self.model().itemFromIndex(index)
        
        labels = self.selected_item.data(Qt.UserRole)

        self.selected_fpath = labels[0]
        self.is_dir_selected = labels[1]

        self.file_clicked.emit({
            'file_path': self.selected_fpath,
            'is_dir': self.is_dir_selected
        })

