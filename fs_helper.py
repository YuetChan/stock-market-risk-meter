import os

class fs_helper:
    
    def get_all_filepaths(root_dir):
      file_paths = []
      for root, dirs, files in os.walk(root_dir):
          for file in files:
              file_paths.append(os.path.join(root, file))
  

      return file_paths


# def find_matched_filepaths(
#       all_fpaths, 
#       fpaths):
#     dangling_fpaths = []
#     matched_fpaths = []

#     for fpath in fpaths:
#         if fpath not in all_fpaths:
#           dangling_fpaths.append(fpath)
#         else:
#           matched_fpaths.append(fpath)   


#     return {
#        'dangling_fpaths': dangling_fpaths,
#        'matched_fpaths': matched_fpaths
#     }


# def get_dir_to_files(filepaths, dirpaths):
#     dir_to_files = {}
#     danglings = []
    
#     # Create dictionary mapping dirpaths to empty list
#     for dirpath in dirpaths:
#         dir_to_files[dirpath] = []
    
#     # Loop through filepaths and add to corresponding dirpath key in dictionary
#     for filepath in filepaths:
#         dirpath = os.path.dirname(filepath)

#         if dirpath in dir_to_files:
#             dir_to_files[dirpath].append(filepath)
#         else:
#             danglings.append(filepath)
    

#     # Add dangling files to 'danglings' key in dictionary
#     if danglings:
#         dir_to_files['danglings'] = danglings
        

#     return dir_to_files


# # Iterative imple
# def scan_dirs(root_dir):
#   """
#   Scans the directory specified by dir path and returns a list of dictionaries
#   containing information about each subdirectory found.
#   """
#   dirs = []

#   dirpaths = []
#   dirpaths.append(root_dir)

#   while len(dirpaths) > 0:
#     path = dirpaths.pop()

#     with os.scandir(path) as it:
#       for entry in it:
#         if entry.is_file():
#           dir_info = {
#             'name': entry.name,
#             'path': entry.path,
#             'size': get_dir_size(entry.path),
#             'last_modified': entry.stat().st_mtime
#           }

#           dirs.append(dir_info)
#           dirpaths.append(entry.path)


#   return dirs


# def get_dir_size(path):
#   """
#   Calculates and returns the total size of a dir and its contents.
#   """
#   total_size = 0

#   for dirpath, dirnames, fnames in os.walk(path):
#     for f in fnames:
#       fp = os.path.join(dirpath, f)
#       total_size += os.path.getsize(fp)

#   return total_size