import filetype
import os
import datetime
import glob
import pickle
import json
# PDF exif tool
from pypdf import PdfReader
# Image exif tools
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Photon
# Office 2007+ decoders
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
# audio and video metadata
from tinytag import TinyTag
import pprint

def save_to_pickle(data, base_file_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_file_path}_{timestamp}.pkl"
    with open(filename, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

def load_and_print(file_path):
    pp = pprint.PrettyPrinter(indent=2)
    temp = None
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            temp = json.load(json_file)
            
    elif file_path.endswith('pkl'):
        with open(file_path, 'rb') as pickle_file:
            temp = pickle.load(pickle_file)


## remove binary data before writing to json
def clean_for_json(data):
    if isinstance(data, dict):
        return {k: clean_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_for_json(v) for v in data]
    elif isinstance(data, bytes):
        return data.decode('utf-8', 'ignore')  # Decoding bytes to string
    elif isinstance(data, datetime.datetime):
        return data.isoformat()  # Converting datetime objects to ISO format string
    return data

# save to json as human-readable
def save_to_json(data, base_file_path):
    #print('-----JSON-----')
    #print(data)
    #print('-----END JSON----')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_file_path}_{timestamp}.json"
    
    cleaned_data = clean_for_json(data)
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(cleaned_data, json_file, ensure_ascii=False, indent=2)

## process a folder and save output
def main_process_folder(folder_path, recursive, save_type):
    metadata_results = {}
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                metadata = extract_metadata(file_path)
                print(metadata)
                if metadata == {}:
                    continue
                metadata_results[file_path] = metadata
    else:
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                file_path = os.path.join(folder_path, file)
                print(file_path)
                metadata = extract_metadata(file_path)
                print(metadata)
                if metadata == {}:
                    continue
                metadata_results[file_path] = metadata

    
    # Save results with timestamp in filenames
    base_path = 'metadata_results'
    match save_type :
        case "pickle" : save_to_pickle(metadata_results, base_path)
        case "json" : save_to_json(metadata_results, base_path)


def extract_metadata(file_path):

    ## known extensions
    image_formats = {ext: get_image_metadata for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg']}
    office_formats = {ext: get_office_metadata for ext in ['xlsx', 'docx', 'pptx']}
    # old_office_formats = {ext: get_old_office_metadata for ext in ['xls', 'doc', 'ppt']}
    video_formats = {ext: get_video_metadata for ext in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv']}
    audio_formats = {ext: get_audio_metadata for ext in ['mp3', 'wav', 'aac', 'ogg', 'flac']}
    
    # Merge all the dictionaries together
    extension_to_function = {
        **image_formats,
        'pdf': get_pdf_metadata,
        **office_formats,
        # **old_office_formats,
        **video_formats,
        **audio_formats
    }

    os_stats = get_readable_file_stats(file_path)
    ## get real file extension
    ## can print message (optional)
    real_extension, given_extension, message = check_file_integrity(file_path)
    if real_extension == None:
        return {}


    ## look through dict of known extensions, run associated function
    metadata_function = extension_to_function.get(real_extension)

    if metadata_function:
        exif_data =  metadata_function(file_path)
    else:
        return "Unsupported file type"

    metadata = { **os_stats, **exif_data }

    metadata = remove_none_entries(metadata)

    return metadata



### remove empty dictionary items
def remove_none_entries(metadata):
    # Remove None entries from the main dictionary
    cleaned_metadata = {k: v for k, v in metadata.items() if v is not None}

    # Check if 'Full' key exists and clean its nested dictionary
    if 'Full' in cleaned_metadata:
        cleaned_metadata['Full'] = {k: v for k, v in cleaned_metadata['Full'].items() if v is not None and v != "" }

    return cleaned_metadata


def check_file_integrity(file_path):
    kind = filetype.guess(file_path)
    print(kind)
    message = ''
    if kind is None :
        message = "Unknown or unsupported image type."
        return None,None,message
    actual_type = kind.extension
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')

    if actual_type == file_extension:
        message = "OK. File is {}".format(file_extension)
    else:
        message = "!! NOK !! File is actually {}".format(actual_type)
    
    return actual_type, file_extension, message


def get_readable_file_stats(filename):
    file_stats = os.stat(filename)
    
    # Convert times from epoch to human-readable format
    readable_stats = {
        "mode": file_stats.st_mode, #specifies the type and mode bits (permissions) of the file
        "ino": file_stats.st_ino, # the Unix inode number and Windows file index
        "dev": file_stats.st_dev, #device identifier on which this specified file resides
        "nlink": file_stats.st_nlink, # hard link number
        "uid": file_stats.st_uid, # uid of owner
        "gid": file_stats.st_gid, # guid of owner 
        "size": file_stats.st_size, # file size
        "access_time": datetime.datetime.fromtimestamp(file_stats.st_atime).strftime("%Y-%m-%d %H:%M:%S"),
        "modify_time": datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "create_time": datetime.datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    }

    return readable_stats

def get_pdf_metadata(filename):

    interesting_objects=("/Title",
                         "/Creator",
                         "/Author",
                         "/Keywords"
                         "/CreationDate",
                         "/ModDate",
                         "/Producer",
                         "/Subject",
                         )
    
    reader = PdfReader(filename)
    meta = reader.metadata
    res = {}
    
    if meta:
        for key in interesting_objects:
            if key in meta:
                res[key[1:]] = meta[key]  # Remove leading '/' and add to dictionary

    # Add full metadata under the key 'Full'
    res['Full'] = dict(meta) if meta else None

    return res


def get_image_metadata(img_src):
    def get_exif(filename):
        image = Image.open(filename)
        #image.verify() ## causes problems with PNG files...
        return image._getexif()

    def get_labeled_exif(exif):
        labeled = {}
        for (key, val) in exif.items():
            labeled[TAGS.get(key)] = val
        return labeled

    def get_geotagging(exif):
        geotagging = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo' and idx in exif:
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]
                return geotagging
        return None

    def get_decimal_from_dms(dms, ref):
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 5)

    def get_coordinates(geotags):
        lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
        lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
        return (lat, lon)

    def get_address(coords):
        locator = Photon(user_agent="measurements")
        location = locator.reverse("{}, {}".format(coords[0], coords[1]))
        return location.address if location else "Address not found"

    # Main functionality
    try:
        exif = get_exif(img_src)
    except:
        return {}

    try:
        labeled_exif = get_labeled_exif(exif)
    except:
        return {}
    geotags = get_geotagging(exif)
    result = {'Full': labeled_exif}

    if geotags:
        coords = get_coordinates(geotags)
        result['Coordinates'] = coords
        result['Address'] = get_address(coords)
        result['GPSTimeStamp'] = geotags.get('GPSTimeStamp', 'Not available')
        result['GPSDateStamp'] = geotags.get('GPSDateStamp', 'Not available')

    return result

### Microsoft office metadata
## Office 2007 and after
def get_office_metadata(file_path):
    extension = file_path.split('.')[-1].lower()

    interesting_attributes = [
        "title", "subject", "creator", "keywords", "last_modified_by",
        "created", "modified", "category", "description", "language"
    ]

    if extension == 'docx':
        doc = Document(file_path)
        properties = doc.core_properties
    elif extension == 'xlsx':
        workbook = load_workbook(file_path, data_only=True)
        properties = workbook.properties
    elif extension == 'pptx':
        presentation = Presentation(file_path)
        properties = presentation.core_properties
    else:
        return "Unsupported file extension"

    # Extract all metadata
    full_metadata = {attr: getattr(properties, attr) for attr in dir(properties)
                     if not attr.startswith('_') and not callable(getattr(properties, attr))}

    # Extract interesting metadata
    metadata = {attr: getattr(properties, attr) for attr in interesting_attributes
                if hasattr(properties, attr)}

    # Add full metadata
    metadata['Full'] = full_metadata

    return metadata

## recursive clean metadata for tinytag
def recursive_clean_metadata(data):
    if isinstance(data, dict):
        return {k: recursive_clean_metadata(v) for k, v in data.items() if not callable(v)}
    elif isinstance(data, list):
        return [recursive_clean_metadata(v) for v in data if not callable(v)]
    else:
        return data

def get_audio_metadata(file_path):

    try:
        tag = TinyTag.get(file_path)
        # Creating a dictionary of all metadata
        full_metadata = {attr: getattr(tag, attr, None) for attr in dir(tag) if not attr.startswith('_') and not callable(getattr(tag, attr))}

        # Extract specific metadata
        metadata = {
            "Title": tag.title,
            "Artist": tag.artist,
            "Album": tag.album,
            "Year": tag.year,
            "Genre": tag.genre,
            "Duration": tag.duration,  # Duration in seconds
        }
        
        # Add full metadata
        metadata['Full'] = full_metadata

        return metadata
        
    except Exception as e:
        return f"Error processing file: {e}"

def get_video_metadata(file_path):

    try:
        tag = TinyTag.get(file_path)
        # Creating a dictionary of all metadata
        full_metadata = {attr: getattr(tag, attr, None) for attr in dir(tag) if not attr.startswith('_') and not callable(getattr(tag, attr))}

        # Extract specific metadata
        metadata = {
            "Title": tag.title,
            "Artist": tag.artist,
            "Album": tag.album,
            "Year": tag.year,
            "Genre": tag.genre,
            "Duration": tag.duration,  # Duration in seconds
        }
        
        # Add full metadata
        metadata['Full'] = recursive_clean_metadata(full_metadata)
        #metadata['Full'] = full_metadata

        return metadata
        
    except Exception as e:
        return f"Error processing file: {e}"



