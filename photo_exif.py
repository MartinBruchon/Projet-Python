from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import reverse_geocode
import geopy
from geopy.geocoders import Photon
#below needed if making lots of requests
#from geopy.extra.rate_limiter import RateLimiter

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
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):
    #print(dms,ref)
    #degrees = dms[0][0] / dms[0][1]
    #minutes = dms[1][0] / dms[1][1] / 60.0
    #seconds = dms[2][0] / dms[2][1] / 3600.0
    
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
    
    return (lat,lon)

def get_addy(coords):
    
    locator = Photon(user_agent="measurements")
    #alternative locator: Nominatim, not working
    #from geopy.geocoders import Nominatim
    #locator = Nominatim(user_agent='myGeocoder', timeout=10)
    
    #ex coordinates = "47.38963, 8.54938"

    coor_string = "{}, {}".format(coords[0], coords[1])
    location = locator.reverse(coor_string)
    res =  location.address
    return res

def analyze_photo(file):
    exif = get_exif(file)
    #label = get_labeled_exif(exif)
    tags = get_geotagging(exif)
    coords = get_coordinates(tags)
    addy = get_addy(coords)

    #print(coords)
    #print(addy)

    ## dictionary: 
    # {"exif_raw" : xxx
    # "gps": (123,123)
    # "address": "123 abc" 
    # "exif_tags": xxx } tags, coords, addy

    return {"exif_raw":exif, "exif_tags":tags, "gps":coords, "address":addy}

