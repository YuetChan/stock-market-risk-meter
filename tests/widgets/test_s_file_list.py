import sys
import os
import unittest

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QSignalSpy

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_file_list import s_file_list

class test_s_file_tree(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        model = QStandardItemModel()

        model.appendRow(QStandardItem(os.path.abspath(__file__)))

        self.s_file_list = s_file_list(model)

        self.spy = QSignalSpy(self.s_file_list.file_clicked)


    def tearDown(self):
        self.app.quit()


    def test_click_first_file_should_emit_click_event(self):
        self.s_file_list.click_first_file()

        self.assertEqual(len(self.spy), 1)


    def test_click_first_file_should_update_current_index_to_first_index(self):
        self.s_file_list.click_first_file()

        self.assertEqual(
            self.s_file_list.currentIndex(), 
            self.s_file_list.model().index(0, 0, QModelIndex())
            )


    def test_click_file_by_index_should_emit_click_event(self):
        self.s_file_list.click_file_by_index(
            self.s_file_list.model().index(0, 0, QModelIndex())
            )

        self.assertEqual(len(self.spy), 1)


    def test_click_file_by_index_should_update_current_index_to_test_index(self):
        self.s_file_list.click_file_by_index(
            self.s_file_list.model().index(0, 0, QModelIndex())
            )

        self.assertEqual(
            self.s_file_list.currentIndex(), 
            self.s_file_list.model().index(0, 0, QModelIndex())
            )

