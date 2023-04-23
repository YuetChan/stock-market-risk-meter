class core_helper:

    def __init__(
            self, 
            config_reader
            ):
        self.config_reader = config_reader


    def add_note_by_filepath(
            self, 
            note, 
            plain_text_note,
            fpath
            ):
        data = self.config_reader.get_data_source()
        data['file_paths'][fpath] = {
            'note': note,
            'plain_text_note': plain_text_note
        }

        self.config_reader.update_data_soruce(data)


    def select_filepaths_with_non_empty_plain_text_note_by_filepaths_in(self, fpaths):
        fpath_json = self.config_reader.get_data_source()['file_paths'].items()

        _fpaths = []

        for k, v in fpath_json:
            if v['plain_text_note'] != '' and k in fpaths:
                _fpaths.append(k)


        return _fpaths


    def select_filepaths_with_non_empty_plain_text_note_by_filepaths_not_in(self, fpaths):
        fpath_json = self.config_reader.get_data_source()['file_paths'].items()

        _fpaths = []

        for k, v in fpath_json:
            if v['plain_text_note'] != '' and not k in fpaths:
                _fpaths.append(k)


        return _fpaths


    def select_note_by_filepath(
            self, 
            fpath
            ):
        if fpath in self.config_reader.get_data_source()['file_paths']:
            return self.config_reader.get_data_source()['file_paths'][fpath]
        else:
            return None

