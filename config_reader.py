import json

class config_reader:

    def __init__(
            self, 
            fname
            ):
        print(fname)
        with open(fname, 'r') as f:
            try:
                json_obj = json.load(f)
                print(json_obj)
                if isinstance(json_obj, dict):
                    self.data = json_obj

                else:
                    print("'data' is not a valid JSON object")


            except json.JSONDecodeError:
              print("'data' is not a valid JSON object")


    def get_project_id(self):
        return self.data['id']


    def get_project_name(self):
        return self.data['name']


    def get_all_filepaths(self):
        return self.data['filepaths']


    def get_data_source(self):
        return self.data


    def create_new_config(dir):
        return ''