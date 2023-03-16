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

        self.file_tree.file_clicked.connect(lambda data : self.open_note(data['file_path'], data['is_dir']))
        self.text_edit_area.text_changed.connect(lambda data : self.auto_save_note(data))

        self.core_helper = core_helper

        self.open_note(self.file_tree.root_dir, True)


    def open_note(self, fpath, is_dir):
        text_edit_area_label = self.text_edit_area_label

        text_edit_area = self.text_edit_area
        text_edit_tool_bar = self.text_edit_tool_bar

        note = self.core_helper.select_note_by_filepath_n_project_id(fpath, self.project_id)

        text_edit_area_label.setText(f'Directory :   {fpath}' if is_dir else f'File :   {fpath}' )

        if note != None:
            text_edit_area.setReadOnly(False)
            text_edit_area.setStyleSheet("background-color: #FFFFFF;")

            text_edit_area.setHtml(note)

        else:
            text_edit_area.setHtml('')

            if is_dir:
                text_edit_area.setReadOnly(True)
                text_edit_area.setStyleSheet("background-color: #f0f0f0;")

                text_edit_tool_bar.disable_all_actions()

            else:
                text_edit_area.setReadOnly(False)
                text_edit_area.setStyleSheet("background-color: #FFFFFF;")  

                text_edit_tool_bar.default_all_actions()


        return


    def auto_save_note(self, data):
        self.save_note(self.file_tree.curr_fpath)


    def save_note(self, fpath):
        self.core_helper.add_note_by_filepath_n_project_id(
            self.text_edit_area.document().toHtml(), 
            fpath, 
            self.project_id
            )
        return
    

