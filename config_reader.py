import json

class config_reader:

    def __init__(
            self, 
            fpath
            ):
        self.fpath = fpath

        with open(self.fpath, 'r') as f:
            try:
                json_obj = json.load(f)

                if isinstance(json_obj, dict):
                    self.data = json_obj
                    self.is_valid = self.data['id'] != None and self.data['name'] != None

                else:
                    self.is_valid = False


            except json.JSONDecodeError:
                self.is_valid = False


    def get_project_id(self):
        return self.data['id']


    def get_project_name(self):
        return self.data['name']


    def get_note(self, fpath):
        return self.data[fpath]['note']
    

    def get_plain_text_note(self, fpath):
        return self.data[fpath]['plain_text_note']


    def get_data_source(self):
        return self.data


    def update_data_soruce(self, data):
        with open(self.fpath, 'w') as outfile:
            json.dump(data, outfile)


    def create_new_config(dir):
        return ''
    


    
