import os
import filetype

# Conversion dictionnary between the type of the file and its category
type_parser = {
    "Image" : ["png","jpg","jpeg", "gif"],
    "PowerPoint Presentation" : ["ppt", "pptx"],
    "Excel" : ["xls", "xlsx"],
    "Word Document" : ["doc", "docx"],
    "Video" : ["mp4", "webp", "mov", "avi", "webm"],
    "Audio File" : ["mp3", "wav"],
    "PDF Document" : ["pdf"]
}

def get_key_from_extension(extension):
    """Get the class in function of the extension of the file
    Args:
        extension (str): The extension of the file. ex:'png'
    Returns:
        str: The class of the file. ex:'Image'
    """    
    for key, value in type_parser.items():
        if extension in value:
            return key
    return None

def get_filetype(file_path):
    """Get the real type of a file
    Args:
        file_path (str): The path of the file
    Returns:
        str: The real type of the file
    """    
    return filetype.guess(file_path).extension

def check_file_integrity(file_path):
    """Crucial method to check for the integrity of the file. Compare the extension to the realtype of the file to validate or not the integrity
    Args:
        file_path (str): Path to the file
    Returns:
        str, str, str: The real type, the extension and the integrity flag of the file
    """    
    kind = filetype.guess(file_path)
    if kind is None:
        return None, None, False
    actual_type = kind.extension
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')
    
    if file_extension == "jpeg" : file_extension = "jpg" # JPEG file are JPG files

    if actual_type == file_extension:
        integrity = True
    else:
        integrity = False
    
    return actual_type, file_extension, integrity

def scan(folder_path):
    """Scan the folder and return the list of the different files in this folder ordered by their type
    Args:
        folder_path (str): Path of the working folder
    Returns:
        dict: Dictionnairy of the different possible file types and the associated files of the folder
    """    
    files_list = {"PDF Document":[],
              "Image":[], 
              "Video":[],
              "Audio File":[],
              "Word Document":[],
              "PowerPoint Presentation":[],
              "Excel":[],
              "Integrity check failure or unsupported file":[]}
    
    # Scan the folder, check the integrity of the files and store the file names into the good category
    for file in os.listdir(folder_path):
        full_path = folder_path + "/" + file
        if os.path.isfile(full_path) :
            file_type,_,integrity = check_file_integrity(full_path)
            if integrity == 1 :
                file_type = get_key_from_extension(file_type)
                try : files_list[file_type].append(file)
                except : continue
            else : files_list["Integrity check failure or unsupported file"].append(file)
        else : pass
    files_list = {key: value for key, value in files_list.items() if value != []}
    return files_list
        