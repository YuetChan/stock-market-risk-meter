from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QTextListFormat, QTextCursor
from PyQt5.QtWidgets import QTextEdit

class s_text_edit_area(QTextEdit):

    def __init__(
            self, 
            parent=None
            ):
        super(s_text_edit_area, self).__init__(parent)

        self.cursorPositionChanged.connect(self.on_cursor_position_changed)


    def set_tool_bar(
            self, 
            tool_bar
            ):
        self.tool_bar = tool_bar


    # Contains custom imple for conifguring list deletion
    def keyPressEvent(
            self, 
            event: QKeyEvent
            ):
        cursor = self.textCursor()

        tool_bar = self.tool_bar

        is_delete_key = event.key() == Qt.Key_Backspace

        # Check if the cursor is at the start of the line
        is_start_of_line = cursor.positionInBlock() == 0

        # Check if the current line is part of a list
        is_list = cursor.currentList() != None

        # If backspace is pressed and the cursor is at the start of the line and the current line is not part of a list
        if is_delete_key and is_start_of_line and not is_list:
            # Check if there is a list in the line above
            is_list_above = self.is_list_above(cursor)

            # Delete current block and the line above as well if line above is part of list and empty
            super().keyPressEvent(event)

            # This condition stops the list in the above line from being deleted
            if is_list_above:
                list_format = QTextListFormat()
                list_format.setStyle(QTextListFormat.ListDisc)

                cursor.createList(list_format)

                tool_bar.action_map['bullet_action'].setChecked(True)

        else:
            # Delete current block and cursor moved to line above
            super().keyPressEvent(event)

            # Check if the current line is not part of a list but the bullet point action in the toolbar is still checked
            is_list = cursor.currentList() != None
            was_in_bullet_pt = not is_list and tool_bar.action_map['bullet_action'].isChecked()

            # This condition implies there was a list piror to the deletion
            if is_delete_key and was_in_bullet_pt:
                self.reset_indent(cursor)

                tool_bar.action_map['bullet_action'].setChecked(False)

                
    def is_list_above(self, cursor):
        cursor.movePosition(QTextCursor.Up)
        is_list_above = cursor.currentList() != None
        
        cursor.movePosition(QTextCursor.Down)

        return is_list_above


    def reset_indent(self, cursor):
        block_format = cursor.blockFormat()
        block_format.setIndent(0)

        cursor.setBlockFormat(block_format)
           
        self.setTextCursor(cursor)


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

