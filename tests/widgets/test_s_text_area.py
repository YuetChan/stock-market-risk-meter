import sys
import os
import unittest

from unittest.mock import MagicMock

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_text_area import s_text_area

class test_s_text_area(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        self.text_area = s_text_area()

        cursor = self.text_area.textCursor()
        cursor.setPosition = MagicMock()
        
        self.text_area.setTextCursor(cursor)
        self.text_area.setTextCursor = MagicMock()

        self.text_area.setText('test')


    def tearDown(self):
        self.app.quit()

    
    def test_highlight_selection_should_update_text_cursor(self):
        self.text_area.highlight_selection(self.text_area.textCursor(), 1, 4)

        self.text_area.setTextCursor.assert_called_once()

    
    def test_find_next_match_should_return_match_when_match_is_found(self):
        self.assertIsInstance(self.text_area.find_next_match(0, 'test'), QTextCursor)

    
    def test_find_next_match_should_return_none_when_match_is_not_found(self):
        self.assertIsNone(self.text_area.find_next_match(0, 'abc'))

    


        