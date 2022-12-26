import sys

from MetadataImage import MetadataImage

if __name__ == "__main__":
    # WIP
    image = MetadataImage(sys.argv[1])
    print(image.name)
    print("\n")
    print(image.metadata)
    print("\n")
    print(image.GPS_metadata)
    image.save_copy_without_metadata()
