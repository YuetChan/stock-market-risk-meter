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

        self._init_actions()


    def is_bullet_pt_checked(self):
        return self.action_map['bullet_action'].isChecked()
    

    def toggle_bullet_pt(self, checked):
        self.action_map['bullet_action'].setChecked(checked)


    def disable_all_actions(self):
        for action in self.action_map.values():
            action.setEnabled(False)
            action.setChecked(False)


    def default_all_actions(self):
        for action in self.action_map.values():
            action.setEnabled(True)
            action.setChecked(False)


        self.action_map['left_align_action'].setChecked(True)


    def _init_actions(self):
        self._init_bold_action()
        self._init_italic_action()
        self._init_underline_action()

        self._init_bullet_point_action()
        
        self._init_left_align()
        self._init_center_align()
        self._init_right_align()

        self._init_redo_action()
        self._init_undo_action()


    def _init_bold_action(self):
        action = QAction(QIcon().fromTheme('format-text-bold'), 'Bold', self)
        
        action.triggered.connect(
            lambda checked: self._set_text_style('bold', checked)
            )
        
        action.setCheckable(True)
        action.setToolTip('Bold')

        self.addAction(action)
        self.action_map['bold_action'] = action


    def _init_italic_action(self):
        action = QAction(QIcon().fromTheme('format-text-italic'), 'Italic', self)
        
        action.triggered.connect(
            lambda checked: self._set_text_style('italic', checked))
        action.setCheckable(True)

        action.setToolTip('Italic')

        self.addAction(action)
        self.action_map['italic_action'] = action


    def _init_underline_action(self):
        action = QAction(QIcon().fromTheme('format-text-underline'), 'Underline', self)
        
        action.triggered.connect(
            lambda checked: self._set_text_style('underline', checked)
            )
        
        action.setCheckable(True)
        action.setToolTip('Underline')

        self.addAction(action)   
        self.action_map['underline_action'] = action


    def _init_bullet_point_action(self):
        action = QAction(QIcon('./resources/list-solid.svg'), 'Bullet Points', self)
        
        action.triggered.connect(
            lambda checked: self._add_bullet_point(checked)
            )

        action.setCheckable(True)
        action.setToolTip('Bullet Points')

        self.addAction(action)
        self.action_map['bullet_action'] = action


    def _init_left_align(self):
        action = QAction(QIcon().fromTheme('format-justify-left'), 'Align Left', self)
        
        action.triggered.connect(
            lambda: self._set_text_alignment('left')
            )
        
        action.setCheckable(True)
        action.setChecked(True)

        action.setToolTip('Left Align')

        self.addAction(action)
        self.action_map['left_align_action'] = action


    def _init_center_align(self):
        action = QAction(QIcon().fromTheme('format-justify-center'), 'Align Center', self)
        
        action.triggered.connect(
            lambda: self._set_text_alignment('center')
            )
        
        action.setCheckable(True)
        action.setToolTip('Center Align')

        self.addAction(action)
        self.action_map['center_align_action'] = action


    def _init_right_align(self):   
        action = QAction(QIcon().fromTheme('format-justify-right'), 'Align Right', self)
        
        action.triggered.connect(
            lambda: self._set_text_alignment('right')
            )
        
        action.setCheckable(True)
        action.setToolTip('Right Align')

        self.addAction(action)
        self.action_map['right_align_action'] = action


    def _init_undo_action(self):
        action = QAction(QIcon('./resources/rotate-left-solid.svg'), 'Undo', self)

        action.triggered.connect(self.text_edit_area.undo)

        action.setShortcut('Ctrl+Z')
        action.setToolTip('Undo')

        self.addAction(action)
        self.action_map['undo_action'] = action


    def _init_redo_action(self):
        action = QAction(QIcon('./resources/rotate-right-solid.svg'), 'Redo', self)

        action.triggered.connect(self.text_edit_area.redo)
        
        action.setShortcut('Ctrl+Y')
        action.setToolTip('Redo')

        self.addAction(action)
        self.action_map['redo_action'] = action


    def _set_text_style(
            self, 
            style, 
            checked=True
            ):
        cursor = self.text_edit_area.textCursor()

        char_fmt = cursor.charFormat()
        font = char_fmt.font()

        if style == 'bold':
            font.setWeight(QFont.Bold if checked else QFont.Normal)

        elif style == 'italic':
            font.setItalic(checked)

        elif style == 'underline':
            font.setUnderline(checked)


        char_fmt.setFont(font)
        self.text_edit_area.setCurrentCharFormat(char_fmt)


    def _set_text_alignment(
            self, 
            alignment
            ):
        if alignment == 'left':
            self.text_edit_area.setAlignment(Qt.AlignLeft)

            self.action_map['right_align_action'].setChecked(False)
            self.action_map['center_align_action'].setChecked(False)

        elif alignment == 'center':
            self.text_edit_area.setAlignment(Qt.AlignCenter)

            self.action_map['right_align_action'].setChecked(False)
            self.action_map['left_align_action'].setChecked(False)

        elif alignment == 'right':
            self.text_edit_area.setAlignment(Qt.AlignRight)

            self.action_map['left_align_action'].setChecked(False)
            self.action_map['center_align_action'].setChecked(False)


    def _add_bullet_point(
            self, 
            checked=True
            ):
        cursor = self.text_edit_area.textCursor()

        if checked:
            list_fmt = QTextListFormat()

            list_fmt.setStyle(QTextListFormat.ListDisc)

            if len(cursor.block().text()) == 0:
                cursor.movePosition(QTextCursor.StartOfBlock)


            cursor.createList(list_fmt)

