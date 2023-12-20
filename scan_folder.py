import os

import filetype
def check_file_integrity(file_path):
    kind = filetype.guess(file_path)
    message = ''
    if kind is None:
        message = "Unknown or unsupported image type."
    actual_type = kind.extension
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')

    if actual_type == file_extension:
        message = True
    else:
        message = False
    
    return actual_type, file_extension, message

class dict(dict):
    def add_file(self, type, file):
        if type in files_list.keys():
            files_list[type].append(file)
        else:
            files_list[type] = [file]
        return files_list

files_list = dict()

def get_file_type(file):
    real_type, ext, integrity = check_file_integrity(file)
    return real_type, integrity

def scan(dossier):
    for file in os.listdir(dossier):
        file_type, integrity = get_file_type(dossier + "/" + file)
        if integrity == 1 :
            files_list.add_file(file_type, file)
        else : files_list.add_file("INTEGRITY NOT SURE", file)
    return files_list