from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QTextEdit

from widgets.s_find_dialog import s_find_dialog

# This class inherits QTextEdit 
# and provides highlight_selection ,find_next_match and get_match_count implementation

# It also display find dialog when ctrl + f
class s_text_area(QTextEdit):

    text_changed = pyqtSignal(dict)

    def __init__(
            self, 
            parent=None
            ):
        super(s_text_area, self).__init__(parent)

        
    def highlight_selection(
            self, 
            cursor, 
            start_pos, 
            end_pos
            ):
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
        
        self.setTextCursor(cursor)


    def find_next_match(
            self, 
            start_pos, 
            search_text
            ):
        match = self.document().find(search_text, start_pos)

        if not match.isNull():
            return match

        else:
            return None   
        

    def get_match_count(
            self, 
            search_text
            ):
        match_count = 0
        init_pos = 0

        while True:
            match = self.document().find(search_text, init_pos)

            if match.isNull():
                break


            init_pos = match.position()
            match_count += 1


        return match_count


    def keyPressEvent(
            self, 
            event: QKeyEvent
            ):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self._show_search_dialog()

        else:
            super().keyPressEvent(event)


    def _show_search_dialog(self):
        s_find_dialog(self).exec_()


    
