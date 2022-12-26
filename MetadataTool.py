import argparse
import sys

from MetadataImage import MetadataImage

parser = argparse.ArgumentParser(
    prog="Image Metadata Tool",
    description="A small tool for viewing and stripping EXIF metadata from images.",
)

parser.add_argument("path")
parser.add_argument("-l", "--list", action="store_true")
parser.add_argument("-g", "--gps", action="store_true")
parser.add_argument("-s", "--strip", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    # WIP
    image = MetadataImage(sys.argv[1])
    print(image.name)
    print("\n")
    print(image.metadata)
    print("\n")
    print(image.GPS_metadata)
    image.save_copy_without_metadata()
