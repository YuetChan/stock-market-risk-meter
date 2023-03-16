import json

class config_reader:

    def __init__(
            self, 
            fname
            ):
        with open(fname, 'r') as f:
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


    def get_data_source(self):
        return self.data


    def create_new_config(dir):
        return ''