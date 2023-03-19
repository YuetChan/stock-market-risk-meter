from PyQt5.QtCore import QModelIndex

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

        self._init_intra_connect()

        self.file_tree.expand(self.file_tree.model().index(0, 0))
        self.file_tree.clicked.emit(self.file_tree.model().index(0, 0, QModelIndex()))

        self.is_file_tree_focused = True
        self.is_file_searcher_focused = False


    def _init_intra_connect(self):
        self.file_tree.file_clicked.connect(
            lambda data : self._open_note(data['file_path'], data['is_dir'], 'file_tree')
            )
    
        self.file_searcher.connect_file_clicked(
            lambda data : self._open_note(data['file_path'], False, 'file_searcher')
            )

        self.text_editor.connect_text_changed(
            lambda data : self._auto_save_note(data)
            )


    def _open_note(self, fpath, is_dir, src):
        self.text_editor.set_label(f'Directory :  {fpath}' if is_dir else f'File :  {fpath}')

        note = self.core_helper.select_note_by_filepath_n_project_id(
            fpath, 
            self.project_id
            )

        if src == 'file_tree':
            self.file_searcher.clear_selection()

            self.default_focus_flags()
            self.is_file_tree_focused = True


        if src == 'file_searcher':
            self.file_tree.clearSelection()
            
            self.default_focus_flags()
            self.is_file_searcher_focused = True


        if note != None:
            self.text_editor.set_html(note[0])
            self.text_editor.default_setting()
            
        else:
            self.text_editor.set_html('')

            if is_dir:
                self.text_editor.set_read_only()

            else:
                self.text_editor.default_setting()


        return

    
    def default_focus_flags(self):
        self.is_file_tree_focused = False
        self.is_file_searcher_focused = False


    def _auto_save_note(self, data):
        is_dir_in_file_tree_selected = self.file_tree.is_dir_selected != None and not self.file_tree.is_dir_selected

        if self.is_file_tree_focused and is_dir_in_file_tree_selected:
            # self._save_note(self.file_tree.selected_fpath)
            print('called')
        elif self.is_file_tree_focused and not is_dir_in_file_tree_selected:
            print('called2')
            # self._save_note(self.file_searcher.selected_fpath)
        else:
            print('called3')


    def _save_note(self, fpath):
        self.core_helper.add_note_by_filepath_n_project_id(
            self.text_editor.to_html(), 
            self.text_editor.to_plain_text(),
            fpath, 
            self.project_id
            )
        
        if not self.text_editor.to_plain_text() == '':
            self.file_tree.highlight_selected_file()

        else:
            self.file_tree.unhighlight_selected_file()
            
    
