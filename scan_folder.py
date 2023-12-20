import os

class dict(dict):
    def add_file(self, type, file):
        if type in files_list.keys():
            files_list[type].append(file)
        else:
            files_list[type] = [file]
        return files_list

files_list = dict()

def get_file_type(file):
    type = file.split(".")[-1]
    return type

def scan(dossier):
    for file in os.listdir(dossier):
        file_type = get_file_type(file)
        files_list.add_file(file_type, file)
    return files_list