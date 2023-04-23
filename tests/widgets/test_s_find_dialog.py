import sys
import os
import unittest

from unittest.mock import MagicMock

from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_text_area import s_text_area
from widgets.s_find_dialog import s_find_dialog

class test_s_find_dialog(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        self.text_area = s_text_area()

        self.text_area.highlight_selection = MagicMock()

        self.find_dialog = s_find_dialog(self.text_area)


    def tearDown(self):
        self.app.quit()


    def test_search_text_should_render_correct_match_count_msg(self):
        self.text_area.setText('test')

        self.find_dialog.search_field.setText('test')
        self.find_dialog.search_text()

        self.assertEqual(self.find_dialog.match_counts_label.text(), 'Match count: 1')


    def test_search_text_should_call_highlight_selection_when_matching_text_is_found(self):
        self.text_area.setText('test')

        self.find_dialog.search_field.setText('test')
        self.find_dialog.search_text()

        self.text_area.highlight_selection.assert_called_once()

    
    def test_search_text_should_not_call_highlight_selection_when_matching_text_is_not_found(self):
        self.text_area.setText('')

        self.find_dialog.search_field.setText('test')
        self.find_dialog.search_text()

        self.text_area.highlight_selection.assert_not_called()

        