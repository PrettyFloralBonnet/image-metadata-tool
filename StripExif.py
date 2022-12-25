import os
import sys
import glob
import exifread

from PIL import Image


def strip_metadata(path):
    file_name = os.path.splitext(path)[0]  # TODO: store this in an instance attr

    try:
        original_image = Image.open(path)
    except IOError:
        print(f"The file {os.path.basename(path)} is not a valid image.")
    
    og_image_data = original_image.getdata()

    new_image = Image.new(original_image.mode, original_image.size)
    new_image.putdata(og_image_data)

    output_dir = os.path.join(os.getcwd(), "output")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    new_image.save(os.path.join(output_dir, f"{file_name}_stripped.JPEG"))

# borrowed from https://gist.github.com/snakeye/fdc372dbf11370fe29eb
def _convert_to_degrees(value):
    """Converts the GPS coordinates stored in the EXIF to degrees.

    :param value: a ratio type value returned by exifread
    :returns a geographical coordinate (latitude or longitude) as a float
    """

    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

# based on https://gist.github.com/snakeye/fdc372dbf11370fe29eb
def getGPS(path):
    """Returns the GPS coordinates, if present.
    
    :param filepath: the path to the file to retrieve the coordinates from
    """

    with open(path, 'rb') as f:
        tags = exifread.process_file(f)  # exifread handles image file validation

        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')

        if latitude is not None:
            latitude = _convert_to_degrees(latitude)
            if latitude_ref.values != 'N':
                latitude = -latitude

        if longitude is not None:
            longitude = _convert_to_degrees(longitude)
            if longitude_ref.values != 'E':
                longitude = -longitude

    return {'latitude': latitude, 'longitude': longitude}

def process_image(path):
    file_name = os.path.splitext(path)[0]  # TODO: retrieve it from an instance attr

    print(getGPS(path))
    strip_metadata(path)
    print(getGPS(os.path.join("output", f"{file_name}_stripped.JPEG")))

if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):  # seems to ignore the output directory
        files = glob.glob(os.path.join(sys.argv[1], "*"))
    else:
        files = sys.argv[1:]

    for im in files:
        process_image(im)
