import os

from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class s_file_tree(QTreeView):

    def __init__(
            self, 
            id, 
            label, 
            root_dir, 
            fpaths, 
            hl_fpaths,
            hl_decorator,
            parent=None
            ):
        super(s_file_tree, self).__init__(parent)

        self.id = id

        self.fpaths = fpaths

        self.hl_fpaths = hl_fpaths
        self.hl_decorator = hl_decorator

        self.setModel(self.populate(root_dir, label))
        self.expand(self.model().index(0, 0))


    def populate(
            self, 
            root_dir,
            label
            ):
        root_item = QStandardItem(root_dir)

        model = QStandardItemModel()

        model.setHorizontalHeaderLabels([label])
        model.appendRow(root_item)

        self.add_files(root_item, root_dir, model)

        return model


    # Recursive impl
    def add_files(
            self, 
            parent, 
            path,
            model
            ):
        fpaths = self.fpaths

        # Loop through the items in the directory
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)

            # If item is a file and in file paths
            if not os.path.isdir(fpath) and fpath in fpaths:
                item = QStandardItem(self.get_filename_with_suffix(fname))

                if fpath in self.hl_fpaths:
                    self.hl_decorator(item)


                parent.appendRow(item)


            # If the item is a directory, recursively add its items
            if os.path.isdir(fpath):
                item = QStandardItem(fname)
                parent.appendRow(item)

                self.add_files(item, fpath, model)


    def decorate_item(
            self, 
            item
            ):
        self.hl_decorator(item)


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


    def get_filename_with_suffix(
            self, 
            name
            ): 
        return os.path.splitext(name)[0] + os.path.splitext(name)[1]

