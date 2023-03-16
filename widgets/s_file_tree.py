import os

from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class s_file_tree(QTreeView):

    file_clicked = pyqtSignal(dict)

    def __init__(
            self, 
            id, 
            label, 
            root_dir, 
            hl_fpaths,
            hl_decorator,
            parent=None
            ):
        super(s_file_tree, self).__init__(parent)

        self.curr_fpath = None

        self.id = id

        self.root_dir = root_dir

        self.hl_fpaths = hl_fpaths
        self.hl_decorator = hl_decorator
        

        self.setModel(self._populate(self.root_dir, label))
        self.expand(self.model().index(0, 0))

        self.clicked.connect(self._on_treeview_clicked)


    def get_selected_file(self):
        return self.curr_fpath


    def print_tree(
            self, 
            parent=None, 
            indent=0
            ):
        if not parent:
            parent = self.invisibleRootItem()


        for i in range(parent.rowCount()):
            child = parent.child(i)
            
            print(" " * indent + str(child.text()))
            self.print_tree(child, indent + 2)


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


    # Recursive impl
    def _add_files(
            self, 
            parent, 
            path,
            model
            ):
        # Loop through the items in the directory
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)

            # If item is a file and in file paths
            if not os.path.isdir(fpath):
                item = QStandardItem(fname)
                
                item.setData(QVariant([fpath, False]), Qt.UserRole)

                if fpath in self.hl_fpaths:
                    self._decorate_item(item)


                parent.appendRow(item)


            # If the item is a directory, recursively add its items
            if os.path.isdir(fpath):
                item = QStandardItem(fname)

                item.setData(QVariant([fpath, True]), Qt.UserRole)
                parent.appendRow(item)

                self._add_files(item, fpath, model)


    def _decorate_item(
            self, 
            item
            ):
        self.hl_decorator(item)


    def _on_treeview_clicked(
            self, 
            index
            ):
        item = self.model().itemFromIndex(index)
        
        labels = item.data(Qt.UserRole)

        self.curr_fpath = labels[0]

        self.file_clicked.emit({
            'file_path': labels[0],
            'is_dir': labels[1]
        })

