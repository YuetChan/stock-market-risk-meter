import os

class fs_helper:
    
    def get_all_filepaths(root_dir):
      file_paths = []
      for root, dirs, files in os.walk(root_dir):
          for file in files:
              file_paths.append(os.path.join(root, file))
  

      return file_paths

