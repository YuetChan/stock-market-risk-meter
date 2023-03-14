from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout

class s_find_dialog(QDialog):

    def __init__(
            self, 
            text_edit_area,
            parent=None
            ):
        super(s_find_dialog, self).__init__(parent)

        self.text_edit_area = text_edit_area

        self.match_count = 0
        self.init_pos = 0

        self.setWindowTitle("Find")
        
        layout = QVBoxLayout(self)
        
        # create the search input field
        label = QLabel("Search for:")

        self.search_field = QLineEdit()

        layout.addWidget(label)
        layout.addWidget(self.search_field)
        
        # create the "Find Next" button
        find_button = QPushButton("Find Next")

        find_button.clicked.connect(self.search_text)

        layout.addWidget(find_button)
        
        # create the "Cancel" button
        cancel_button = QPushButton("Cancel")

        cancel_button.clicked.connect(self.reject)

        layout.addWidget(cancel_button)

        self.match_counts_label = QLabel("Match count:")

        layout.addWidget(self.match_counts_label)
        

    def search_text(self):
        cursor = self.text_edit_area.textCursor()

        # if there is a selection, clear it before searching
        if cursor.hasSelection():
            cursor.clearSelection()


        search_text = self.search_field.text()

        self.match_counts_label.setText(f'Match count: {self.get_match_count(search_text)}')

        match = self.find_next_match(self.init_pos, search_text)

        print(match)

        start_pos = match.position() - len(search_text)
        end_pos = match.position()

        self.text_edit_area.highlight_selection(cursor, start_pos, end_pos)

        self.init_pos = end_pos
 

    def find_next_match(
            self, 
            pos, 
            search_text
            ):
        match = self.text_edit_area.document().find(search_text, pos)

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
            match = self.text_edit_area.document().find(search_text, init_pos)

            if match.isNull():
                break


            init_pos = match.position()
            match_count += 1


        return match_count
            
    

