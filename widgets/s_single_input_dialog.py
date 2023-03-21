from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout

class s_single_input_dialog(QDialog):

    def __init__(
            self, 
            input_map,
            parent=None
            ):
        super().__init__(parent)
        
        self.input_map = input_map

        self._init_ui()
        

    def get_config(self): 
        return {
            self.input_map['dialog_var']: self.line_edit.text()
        }


    def _init_ui(self):
        self.setWindowTitle(self.input_map['dialog_title'])
        
        self.label = QLabel(self.input_map['dialog_msg'])

        self.line_edit = QLineEdit()
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)

