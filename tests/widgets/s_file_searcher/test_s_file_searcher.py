import sys
import os
import unittest

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QLabel

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..'))
sys.path.append(parent_dir)

from widgets.s_file_searcher.s_file_searcher import s_file_searcher
from widgets.s_file_list import s_file_list
from widgets.s_search_bar import s_file_search_bar

class test_s_file_searcher(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        self.search_title = QLabel('Dangling Notes')

        self.search_bar = s_file_search_bar()

        model = QStandardItemModel()

        model.appendRow(QStandardItem(os.path.abspath(__file__)))

        self.file_list = s_file_list(model)

        self.file_searcher = s_file_searcher(
            self.search_title, 
            self.search_bar, 
            self.file_list
            )


    def tearDown(self):
        self.app.quit()


    def test_get_file_count_should_return_correct_count(self):
        self.assertEqual(self.file_searcher.get_file_count(), 1)


    def test_has_selection_before_file_click(self):
        self.assertEqual(self.file_searcher.has_selection(), False)


    def test_has_selection_after_file_click(self):
        self.file_searcher.click_first_file()

        self.assertEqual(self.file_searcher.has_selection(), True)


    def test_clear_selection_should_clear_selection(self):
        self.file_searcher.clear_selection()

        self.assertEqual(self.file_searcher.has_selection(), False)


    def test_remove_selected_file(self):
        self.file_searcher.click_first_file()
        self.file_searcher.remove_selected_file()

        self.assertEqual(self.file_searcher.get_file_count(), 0)

