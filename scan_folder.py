import os
import filetype

type_parser = {
    "Image" : ["png","jpg","jpeg"],
    "PowerPoint Presentation" : ["ppt", "pptx"],
    "Excel" : ["xls", "xlsx"],
    "Word Document" : ["doc", "docx"],
    "Video" : ["mp4"],
    "Audio File" : ["mp3"],
    "PDF Document" : ["pdf"]
}

def get_key_from_extension(extension):
    for key, value in type_parser.items():
        if extension in value:
            return key
    return None

def get_filetype(file_path):
    return filetype.guess(file_path).extension

def check_file_integrity(file_path):
    kind = filetype.guess(file_path)
    if kind is None:
        return None, None, False
    actual_type = kind.extension
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')
    
    if file_extension == "jpeg" : file_extension = "jpg"

    if actual_type == file_extension:
        integrity = True
    else:
        integrity = False
    
    return actual_type, file_extension, integrity

class dict(dict):
    def add_file(self, type, file):
        if type in files_list.keys():
            files_list[type].append(file)
        else:
            files_list[type] = [file]
        return files_list

files_list = dict()

def scan(dossier):
    for file in os.listdir(dossier):
        full_path = dossier + "/" + file
        if os.path.isfile(full_path) :
            file_type,_,integrity = check_file_integrity(full_path)
            if integrity == 1 :
                file_type = get_key_from_extension(file_type)
                files_list.add_file(file_type, file)
            else : files_list.add_file("Integrity check failure", file)
        else : pass
    return files_list
        