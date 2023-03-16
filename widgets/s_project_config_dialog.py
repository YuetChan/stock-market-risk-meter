from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout

class s_project_config_dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('New Project')
        
        # Create label and line edit for project name
        self.label = QLabel('Enter project name:')
        self.line_edit = QLineEdit()
        
        # Create button box
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        # Add widgets to layout
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)
        

    def get_project_name(self):
        return self.line_edit.text()