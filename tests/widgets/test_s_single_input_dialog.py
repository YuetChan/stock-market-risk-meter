import sys
import os
import unittest

from PyQt5.QtWidgets import QApplication

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.append(parent_dir)

from widgets.s_single_input_dialog import s_single_input_dialog

class test_s_single_input_dialog(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])

        self.dialog = s_single_input_dialog({
            'dialog_title': 'New Project',
            'dialog_var': 'project_name',
            'dialog_msg': 'Enter a project'
        })


    def tearDown(self):
        self.app.quit()

    
    def test_get_config_should_return_corresponded_config(self):
        self.dialog.line_edit.setText('test')
        
        self.assertEqual(self.dialog.get_config()['project_name'], 'test')

