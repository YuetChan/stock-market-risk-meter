from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMessageBox

class core_manager:
  
    def __init__(
            self,
            project_id,
            file_tree,
            file_searcher,
            text_editor,
            core_helper
            ):
        self.project_id = project_id

        self.file_tree = file_tree
        self.file_searcher = file_searcher
        
        self.text_editor = text_editor

        self.core_helper = core_helper

        self.file_tree.file_clicked.connect(
            lambda data : self._on_file_tree_file_clicked(data['file_path'], data['is_dir'])
            )
    
        self.file_searcher.connect_file_clicked(
            lambda data : self._on_file_searcher_file_clicked(data['file_path'])
            )

        self.text_editor.connect_text_changed(
            lambda data : self._auto_save_note(data)
            )

        self.file_tree.expand(self.file_tree.model().index(0, 0))
        self.file_tree.clicked.emit(self.file_tree.model().index(0, 0, QModelIndex()))

        self.is_file_tree_focused = True
        self.is_file_searcher_focused = False

        self.auto_delete_msg_box = QMessageBox()

        self.auto_delete_msg_box.setText("Would you like to add a placeholder to prevent the automatic deletion of an empty dangling note")
        self.auto_delete_msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.auto_delete_placeholder = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">placeholder</p></body></html>'


    def _on_file_tree_file_clicked(self, fpath, is_dir):
        self.file_searcher.clear_selection()

        self._default_focus_flags()
        self.is_file_tree_focused = True

        self._open_note(fpath, is_dir)


    def _on_file_searcher_file_clicked(self, fpath):
        self.file_tree.clearSelection()

        self._default_focus_flags()
        self.is_file_searcher_focused = True

        self._open_note(fpath, False)


    def _open_note(self, fpath, is_dir):
        self.text_editor.set_label(f'Directory :  {fpath}' if is_dir else f'File :  {fpath}')

        note = self.core_helper.select_note_by_filepath_n_project_id(
            fpath, 
            self.project_id
            )

        if note != None and note[1] != '':
            self.text_editor.set_html(note[0])
            self.text_editor.default_setting()
            
        else:
            self.text_editor.set_html('')

            if is_dir:
                self.text_editor.set_read_only()

            else:
                self.text_editor.default_setting()


        return

    
    def _default_focus_flags(self):
        self.is_file_tree_focused = False
        self.is_file_searcher_focused = False


    def _auto_save_note(self, data):        
        if self.file_tree.selectionModel().hasSelection():
            self._auto_highlight_file_tree_file()
            self._save_note(self.file_tree.selected_fpath)

        elif self.file_searcher.has_selection():
            self._auto_remove_file_searcher_empty_file()
            self._save_note(self.file_searcher.selected_fpath)


    def _auto_highlight_file_tree_file(self):
        if not self.text_editor.to_plain_text() == '':
            self.file_tree.highlight_selected_file()

        else:
            self.file_tree.unhighlight_selected_file()


    def _auto_remove_file_searcher_empty_file(self):
        if self.text_editor.to_plain_text() == '':
            removed = self._prompt_remove_dialog()
            
            if removed == QMessageBox.Yes:
                self.text_editor.set_html(self.auto_delete_placeholder) 

            else:
                self.file_searcher.remove_selected_file()

                if self.file_searcher.get_file_count() > 0:
                    self.file_searcher.select_first_file()     

            
    def _save_note(self, fpath):
        self.core_helper.add_note_by_filepath_n_project_id(
            self.text_editor.to_html(), 
            self.text_editor.to_plain_text(),
            fpath, 
            self.project_id
            )
        

    def _prompt_remove_dialog(self):
        return self.auto_delete_msg_box.exec_()

