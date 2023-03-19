from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

from widgets.s_text_editor.s_text_edit_tool_bar import s_text_edit_tool_bar
from widgets.s_text_editor.s_text_edit_area import s_text_edit_area

class s_text_editor(QWidget):

    def __init__(
            self,
            parent=None
            ):
        super(s_text_editor, self).__init__(parent)

        self.text_edit_area_label = QLabel('')

        self.text_edit_area = s_text_edit_area()

        self.text_edit_tool_bar = s_text_edit_tool_bar(self.text_edit_area)

        v_box = QVBoxLayout()

        v_box.addWidget(self.text_edit_area_label)

        v_box.addWidget(self.text_edit_tool_bar)
        v_box.addWidget(self.text_edit_area)

        self.setLayout(v_box)


    def set_label(
            self, 
            label
            ):
        self.text_edit_area_label.setText(label)


    def is_bullet_pt_checked(self):
        return self.text_edit_tool_bar.action_map['bullet_action'].isChecked()
    

    def toggle_bullet_pt(
            self, 
            checked
            ):
        self.text_edit_tool_bar.action_map['bullet_action'].setChecked(checked)


    def disable_all_actions(self):
        for action in self.text_edit_tool_bar.action_map.values():
            action.setEnabled(False)
            action.setChecked(False)


    def default_all_actions(self):
        for action in self.text_edit_tool_bar.action_map.values():
            action.setEnabled(True)
            action.setChecked(False)


        self.text_edit_tool_bar.action_map['left_align_action'].setChecked(True)


    def connect_text_changed(
            self, 
            l_func
            ):
        self.text_edit_area.text_changed.connect(l_func)

    
    def set_read_only(self):
        self.text_edit_area.setReadOnly(True)
        self.text_edit_area.setStyleSheet("background-color: #f0f0f0;")

        self.text_edit_tool_bar.disable_all_actions()

        
    def default_setting(self):    
        self.text_edit_area.setReadOnly(False)
        self.text_edit_area.setStyleSheet("background-color: #FFFFFF;")  

        self.text_edit_tool_bar.default_all_actions()

    
    def set_html(
            self, 
            html
            ):
        self.text_edit_area.setHtml(html)


    def to_html(self):
        return self.text_edit_area.toHtml()
    

    def to_plain_text(self):
        return self.text_edit_area.toPlainText()
    
