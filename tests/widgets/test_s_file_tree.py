import sys
import os
import unittest

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_file_tree import s_file_tree

class test_s_file_tree(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        dummy_project_name = 'dummy project'
  
        dummy_hl_fpaths = []
        dummy_decorator = lambda item : item.setForeground(QBrush(QColor('green')))

        self.file_tree = s_file_tree(dummy_hl_fpaths, dummy_decorator)

        dummy_root_fpath = os.path.abspath(os.getcwd())

        self.file_tree.setModel(
            self._populate_file_tree_model(dummy_root_fpath, dummy_project_name)
            )


    def tearDown(self):
        self.app.quit()


    def test_highlight_selected_file_should_update_selected_item_foreground_color(self):
        model = self.file_tree.model()

        idx = self.find_index_by_fpath(
            model, 
            model.invisibleRootItem().index(), 
            os.path.abspath(__file__)
            )

        self.file_tree.selected_item = self.file_tree.model().itemFromIndex(idx)
        self.file_tree.highlight_selected_file()

        self.assertEqual(self.file_tree.selected_item.foreground().color(),  QColor('green'))


    def test_unhighlight_selected_file_should_default_selected_item_foreground_color(self):
        model = self.file_tree.model()

        idx = self.find_index_by_fpath(
            model, 
            model.invisibleRootItem().index(), 
            os.path.abspath(__file__)
            )

        self.file_tree.selected_item = self.file_tree.model().itemFromIndex(idx)
        # 'black' is default color
        self.file_tree.selected_item.setForeground(QBrush(QColor('black')))

        self.file_tree.unhighlight_selected_file()

        self.assertEqual(self.file_tree.selected_item.foreground().color(),  QColor('black'))


    @unittest.skip("Skip setUp")
    def test_should_hightlight_specified_file_paths_at_object_creation(self):
        self.app = QApplication([])

        dummy_project_name = 'dummy project'
  
        dummy_hl_fpaths = [os.path.abspath(__file__)]
        dummy_decorator = lambda item : item.setForeground(QBrush(QColor('green')))

        self.file_tree = s_file_tree(dummy_hl_fpaths, dummy_decorator)

        dummy_root_fpath = os.path.abspath(os.getcwd())

        self.file_tree.setModel(
            self._populate_file_tree_model(dummy_root_fpath, dummy_project_name)
            )

        model = self.file_tree.model()

        idx = self.find_index_by_fpath(
            model, 
            model.invisibleRootItem().index(), 
            os.path.abspath(__file__)
            )
        
        hl_item = self.file_tree.model().itemFromIndex(idx)

        self.assertEqual(hl_item.foreground().color(),  QColor('green'))


    def _populate_file_tree_model(
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
                parent.appendRow(item)


            if os.path.isdir(fpath):
                item = QStandardItem(fname)

                item.setData(QVariant([fpath, True]), Qt.UserRole)
                parent.appendRow(item)

                self._add_files(item, fpath, model)

    
    def find_index_by_fpath(
            self, 
            model, 
            parent_idx, 
            fpath
            ):
        for row in range(model.rowCount(parent_idx)):
            idx = model.index(row, 0, parent_idx)
            labels = idx.data(Qt.UserRole)

            if labels[0] == fpath:
                return idx


            if model.hasChildren(idx):
                matched_idx = self.find_index_by_fpath(model, idx, fpath)

                if matched_idx != None:
                    return matched_idx
        

        return None

