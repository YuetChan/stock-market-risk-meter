import sys
import os
import unittest

from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

class test_s_search_bar(unittest.TestCase):
    
    def setUp(self):
        self.app = QApplication([])


    def tearDown(self):
        self.app.quit()

        