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

class test_s_find_dialog(unittest.TestCase):

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