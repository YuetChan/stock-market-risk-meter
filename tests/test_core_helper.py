import sys
import os
import unittest

# Add the parent directory of 'widgets' to the Python system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from config_reader import config_reader

from core_helper import core_helper

class test_core_helper(unittest.TestCase):

    def setUp(self):
        os.environ['code_meta_dir'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_json_fpath = os.environ['code_meta_dir'] + '/tests/test_data.json'

        self.c_helper = core_helper(None, config_reader(test_json_fpath))


    def test_select_filepaths_with_non_empty_plain_text_note_by_filepaths_in(self):
        fpaths = self.c_helper.select_filepaths_with_non_empty_plain_text_note_by_filepaths_in(['filepath3'])
        self.assertEqual('filepath3' in fpaths, True)


    def test_select_filepaths_with_non_empty_plain_text_note_by_filepaths_not_in(self):
        fpaths = self.c_helper.select_filepaths_with_non_empty_plain_text_note_by_filepaths_not_in(['filepath3'])
        self.assertEqual(len(fpaths), 0)

    