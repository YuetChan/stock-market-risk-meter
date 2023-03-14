from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QToolBar
from PyQt5.QtGui import QFont, QTextListFormat, QIcon, QTextCursor

class s_text_edit_tool_bar(QToolBar):

    def __init__(
            self,
            text_edit_area, 
            parent=None
            ):
        super(s_text_edit_tool_bar, self).__init__(parent)

        self.text_edit_area = text_edit_area
        self.text_edit_area.set_tool_bar(self)

        self.action_map = { }

        self.init_ui()


    def set_main_window(
            self, 
            main_window
            ):
        self.main_window = main_window


    def init_ui(self):
        self.init_bold_action()
        self.init_italic_action()
        self.init_underline_action()

        self.init_bullet_point_action()
        # self.init_code_block()
        
        self.init_left_align()
        self.init_center_align()
        self.init_right_align()

        self.init_redo_action()
        self.init_undo_action()


    def init_bold_action(self):
        bold_action = QAction(QIcon().fromTheme('format-text-bold'), 'Bold', self)
        
        bold_action.triggered.connect(
            lambda checked: self.set_text_style('bold', checked))
        bold_action.setCheckable(True)

        self.addAction(bold_action)
        self.action_map['bold_action'] = bold_action


    def init_italic_action(self):
        italic_action = QAction(QIcon().fromTheme('format-text-italic'), 'Italic', self)
        
        italic_action.triggered.connect(
            lambda checked: self.set_text_style('italic', checked))
        italic_action.setCheckable(True)

        self.addAction(italic_action)
        self.action_map['italic_action'] = italic_action


    def init_underline_action(self):
        underline_action = QAction(QIcon().fromTheme('format-text-underline'), 'Underline', self)
        
        underline_action.triggered.connect(
            lambda checked: self.set_text_style('underline', checked))
        underline_action.setCheckable(True)

        self.addAction(underline_action)   
        self.action_map['underline_action'] = underline_action


    def init_bullet_point_action(self):
        bullet_action = QAction(QIcon().fromTheme('format-list-unordered'), 'Bullet Points', self)
        
        bullet_action.setCheckable(True)
        bullet_action.triggered.connect(
            lambda checked: self.add_bullet_point(checked))

        self.addAction(bullet_action)
        self.action_map['bullet_action'] = bullet_action


    # def init_code_block(self):
    #     code_block_action = QAction('Code Block', self)
        
    #     code_block_action.triggered.connect(self.add_code_block)
    #     code_block_action.setCheckable(True)

    #     self.addAction(code_block_action)


    def init_left_align(self):
        left_align_action = QAction(QIcon().fromTheme('format-justify-left'), 'Align Left', self)
        
        left_align_action.triggered.connect(
            lambda: self.set_text_alignment('left'))
        left_align_action.setCheckable(True)
        left_align_action.setChecked(True)

        self.addAction(left_align_action)
        self.action_map['left_align_action'] = left_align_action


    def init_center_align(self):
        center_align_action = QAction(QIcon().fromTheme('format-justify-center'), 'Align Center', self)
        
        center_align_action.triggered.connect(
            lambda: self.set_text_alignment('center'))
        center_align_action.setCheckable(True)

        self.addAction(center_align_action)
        self.action_map['center_align_action'] = center_align_action


    def init_right_align(self):   
        right_align_action = QAction(QIcon().fromTheme('format-justify-right'), 'Align Right', self)
        
        right_align_action.triggered.connect(
            lambda: self.set_text_alignment('right'))
        right_align_action.setCheckable(True)

        self.addAction(right_align_action)
        self.action_map['right_align_action'] = right_align_action


    def init_undo_action(self):
        undo_action = QAction('Undo', self)

        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit_area.undo)

        self.addAction(undo_action)


    def init_redo_action(self):
        redo_action = QAction('Redo', self)

        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit_area.redo)
        
        self.addAction(redo_action)


    def set_text_style(
            self, 
            style, 
            checked=True
            ):
        text_edit_area = self.text_edit_area

        cursor = text_edit_area.textCursor()

        char_format = cursor.charFormat()
        font = char_format.font()

        if style == 'bold':
            font.setWeight(QFont.Bold if checked else QFont.Normal)

        elif style == 'italic':
            font.setItalic(checked)

        elif style == 'underline':
            font.setUnderline(checked)


        char_format.setFont(font)
        text_edit_area.setCurrentCharFormat(char_format)


    def set_text_alignment(
            self, 
            alignment
            ):
        text_edit_area = self.text_edit_area
        action_map = self.action_map

        if alignment == 'left':
            text_edit_area.setAlignment(Qt.AlignLeft)

            action_map['right_align_action'].setChecked(False)
            action_map['center_align_action'].setChecked(False)

        elif alignment == 'center':
            text_edit_area.setAlignment(Qt.AlignCenter)

            action_map['right_align_action'].setChecked(False)
            action_map['left_align_action'].setChecked(False)

        elif alignment == 'right':
            text_edit_area.setAlignment(Qt.AlignRight)

            action_map['left_align_action'].setChecked(False)
            action_map['center_align_action'].setChecked(False)


    def add_bullet_point(
            self, 
            checked=True
            ):
        cursor = self.text_edit_area.textCursor()

        if checked:
            # create a list format
            list_format = QTextListFormat()
            list_format.setStyle(QTextListFormat.ListDisc)

            if len(cursor.block().text()) == 0:
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.StartOfBlock)


            # insert the list format
            cursor.createList(list_format)


    # def add_code_block(self):
    #     cursor = self.text_edit_area.textCursor()

    #     # create a char format and set its text color to red
    #     char_format = QTextCharFormat()

    #     char_format.setForeground(QColor("#D4D4D4"))
    #     char_format.setFont(QFont("Courier", 10, QFont.Normal))

    #     cursor.mergeCharFormat(char_format)

    #     # Create block format for code block
    #     block_format = cursor.blockFormat()
    #     block_format.setBackground(QColor("#2E2E2E"))
        
    #     block_format.setLeftMargin(15)
    #     block_format.setRightMargin(10)

    #     # Apply block and char formats
    #     cursor.mergeBlockFormat(block_format)
        
    #     cursor.select(QTextCursor.LineUnderCursor)

    #     # self.global_char_format = char_format
    #     self.text_edit_area.setCurrentCharFormat(char_format)


    def format_for(
            self, 
            style
            ):
        return self.text_edit_area.document().rootFrame().frameFormat().property(style)
    

    def is_bullet_pt_checked(self):
        return self.action_map['bullet_action'].isChecked()
    

    def toggle_bullet_pt(self, checked):
        self.action_map['bullet_action'].setChecked(checked)

