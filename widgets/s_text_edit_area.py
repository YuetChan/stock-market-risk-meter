from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QTextEdit

class s_text_edit_area(QTextEdit):

    def __init__(
            self, 
            parent=None
            ):
        super(s_text_edit_area, self).__init__(parent)

        self.cursorPositionChanged.connect(self.on_cursor_position_changed)
        self.document().blockCountChanged.connect(self.on_block_count_changed)

    def set_tool_bar(
            self, 
            tool_bar
            ):
        self.tool_bar = tool_bar


    def keyPressEvent(
            self, 
            event: QKeyEvent
            ):
        super().keyPressEvent(event)

        tool_bar = self.tool_bar

        is_delete_key = event.key() == Qt.Key_Backspace
        was_in_bullet_pt = self.textCursor().currentList() == None and tool_bar.action_map['bullet_action'].isChecked()

        if is_delete_key and was_in_bullet_pt:
            tool_bar.action_map['bullet_action'].setChecked(False)

            cursor = self.textCursor()

            block_format = cursor.blockFormat()
            block_format.setIndent(0)

            cursor.setBlockFormat(block_format)
           
            self.setTextCursor(cursor)


    def on_block_count_changed(self):
        


    def on_cursor_position_changed(self):
        cursor = self.textCursor()

        block_format = cursor.blockFormat()

        font = cursor.charFormat().font()

        action_map = self.tool_bar.action_map

        action_map['bold_action'].setChecked(True if font.bold() else False)
        action_map['italic_action'].setChecked(True if font.italic() else False)
        action_map['underline_action'].setChecked(True if font.underline() else False)

        action_map['bullet_action'].setChecked(True if cursor.currentList() else False)

        action_map['left_align_action'].setChecked(True if block_format.alignment() == Qt.AlignLeft else False)
        action_map['center_align_action'].setChecked(True if block_format.alignment() == Qt.AlignCenter else False)
        action_map['right_align_action'].setChecked(True if block_format.alignment() == Qt.AlignRight else False)
   