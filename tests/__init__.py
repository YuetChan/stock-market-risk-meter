import unittest

from widgets.s_file_searcher.test_s_file_searcher import test_s_file_searcher
from widgets.test_s_file_list import test_s_file_list
from widgets.test_s_file_tree import test_s_file_tree
from widgets.test_s_find_dialog import test_s_find_dialog
from widgets.test_s_search_bar import test_s_search_bar
from widgets.test_s_single_input_dialog import test_s_single_input_dialog
from widgets.test_s_text_area import test_s_text_area

suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(test_s_file_searcher))
suite.addTest(unittest.makeSuite(test_s_file_list))
suite.addTest(unittest.makeSuite(test_s_file_tree))
suite.addTest(unittest.makeSuite(test_s_find_dialog))
suite.addTest(unittest.makeSuite(test_s_search_bar))
suite.addTest(unittest.makeSuite(test_s_single_input_dialog))
suite.addTest(unittest.makeSuite(test_s_text_area))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)