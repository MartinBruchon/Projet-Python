import filetype
import os
import glob
from pypdf import PdfReader
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Photon



def check_file_integrity(file_path):
    kind = filetype.guess(file_path)
    message = ''
    if kind is None:
        message = "Unknown or unsupported image type."
    actual_type = kind.extension
    file_extension = os.path.splitext(file_path)[1].lower().strip('.')

    if actual_type == file_extension:
        message = "OK. File is {}".format(file_extension)
    else:
        message = "!! NOK !! File is actually {}".format(actual_type)
    
    return actual_type, file_extension, message

def extract_metadata(file_path):

    ## known extensions
    extension_to_function = {
        # Image Formats
        ext: get_image_metadata for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
        # PDF
        '.pdf': get_pdf_metadata,
        # Microsoft Office Formats
        ext: get_word_doc_metadata for ext in ['.doc', '.docx'],
        ext: get_excel_metadata for ext in ['.xls', '.xlsx'],
        ext: get_powerpoint_metadata for ext in ['.ppt', '.pptx'],
        # Video Formats
        ext: get_video_metadata for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
        # Audio Formats
        ext: get_audio_metadata for ext in ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
    }

    ## get real file extension
    ## can print message (optional)
    real_extension, given_extension, message = check_file_integrity(file_path)

    ## look through dict of known extensions, run associated function
    metadata_function = extension_to_function.get(real_extension)

    if metadata_function:
        return metadata_function(file_path)
    else:
        return "Unsupported file type"


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
    
    reader = PdfReader(d)
    meta = reader.metadata
    res = {}
    
    if meta:
        for key in interesting_objects:
            if key in meta:
                res[key[1:]] = meta[key]  # Remove leading '/' and add to dictionary

    # Add full metadata under the key 'Full'
    res['Full'] = dict(meta) if meta else "No metadata found"

    return res


def get_image_metadata(img_src):
    def get_exif(filename):
        image = Image.open(filename)
        image.verify()
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
    exif = get_exif(img_src)
    if not exif:
        return {}

    labeled_exif = get_labeled_exif(exif)
    geotags = get_geotagging(exif)
    result = {'Full': labeled_exif}

    if geotags:
        coords = get_coordinates(geotags)
        result['Coordinates'] = coords
        result['Address'] = get_address(coords)
        result['GPSTimeStamp'] = geotags.get('GPSTimeStamp', 'Not available')
        result['GPSDateStamp'] = geotags.get('GPSDateStamp', 'Not available')

    return result


