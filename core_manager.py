class core_manager:
  
    def __init__(
            self,
            project_id,
            file_tree,
            text_edit_area_label,
            text_edit_area,
            text_edit_tool_bar,
            core_helper
            ):
        self.project_id = project_id

        self.file_tree = file_tree

        self.text_edit_area_label = text_edit_area_label

        self.text_edit_area = text_edit_area
        self.text_edit_tool_bar = text_edit_tool_bar

        self.core_helper = core_helper

        self._init_intra_connect()

        self._open_note(self.file_tree.root_dir, True)


    def _init_intra_connect(self):
        self.file_tree.file_clicked.connect(
            lambda data : self._open_note(data['file_path'], data['is_dir'])
            )
        
        self.text_edit_area.text_changed.connect(
            lambda data : self._auto_save_note(data)
            )


    def _open_note(self, fpath, is_dir):
        self.text_edit_area_label.setText(
            f'Directory :   {fpath}' if is_dir else f'File :   {fpath}'
            )

        note = self.core_helper.select_note_by_filepath_n_project_id(
            fpath, 
            self.project_id
            )

        if note != None:
            self.text_edit_area.setReadOnly(False)
            self.text_edit_area.setStyleSheet("background-color: #FFFFFF;")

            self.text_edit_area.setHtml(note[0])
            self.text_edit_tool_bar.default_all_actions()

        else:
            self.text_edit_area.setHtml('')

            if is_dir:
                self.text_edit_area.setReadOnly(True)
                self.text_edit_area.setStyleSheet("background-color: #f0f0f0;")

                self.text_edit_tool_bar.disable_all_actions()

            else:
                self.text_edit_area.setReadOnly(False)
                self.text_edit_area.setStyleSheet("background-color: #FFFFFF;")  

                self.text_edit_tool_bar.default_all_actions()


        return


    def _auto_save_note(self, data):
        if self.file_tree.is_dir_selected != None and not self.file_tree.is_dir_selected:
            self._save_note(self.file_tree.selected_fpath)


    def _save_note(self, fpath):
        self.core_helper.add_note_by_filepath_n_project_id(
            self.text_edit_area.document().toHtml(), 
            self.text_edit_area.document().toPlainText(),
            fpath, 
            self.project_id
            )
        
        if not self.text_edit_area.document().toPlainText() == '':
            self.file_tree.decorate_selected_file()

        else:
            self.file_tree.undecorate_selected_file()
            
    