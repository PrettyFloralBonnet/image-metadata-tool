import os
import sys
import exifread

from PIL import Image
from typing import Dict


class MetadataImage:
    def __init__(self, path) -> None:
        self.path = path
        self._metadata = None

    @property
    def name(self) -> str:
        """Returns the name of the image file (without extension)."""

        return os.path.splitext(self.path)[0]

    @property
    def metadata(self) -> Dict:
        """Returns all image metadata."""

        if self._metadata is None:
            with open(self.path, "rb") as im:
                # file type validation is handled internally by exifread
                tags = exifread.process_file(im)
                self._metadata = tags

        return self._metadata

    @staticmethod
    def _convert_GPS_to_degrees(value: exifread.classes.IfdTag) -> float:
        """Converts the GPS coordinates stored in the metadata to degrees.

        :param value: a ratio type value returned by exifread
        :returns a geographical coordinate (latitude or longitude) as a float
        """

        # borrowed from https://gist.github.com/snakeye/fdc372dbf11370fe29eb

        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    @property
    def GPS_metadata(self) -> Dict:
        """Returns GPS related metadata only."""

        # based on https://gist.github.com/snakeye/fdc372dbf11370fe29eb

        latitude = self.metadata.get('GPS GPSLatitude')
        latitude_ref = self.metadata.get('GPS GPSLatitudeRef')
        longitude = self.metadata.get('GPS GPSLongitude')
        longitude_ref = self.metadata.get('GPS GPSLongitudeRef')

        if latitude is not None:
            latitude = self._convert_GPS_to_degrees(latitude)
            if latitude_ref.values != 'N':
                latitude = -latitude

        if longitude is not None:
            longitude = self._convert_GPS_to_degrees(longitude)
            if longitude_ref.values != 'E':
                longitude = -longitude

        return {'latitude': latitude, 'longitude': longitude}

    def save_copy_without_metadata(self) -> None:
        """Saves a copy of the image stripped from all metadata."""

        if len(self.metadata) == 0:
            print(f"The image {self.name} has no metadata. No copy will be created.")
            return

        try:
            image = Image.open(self.path)
        except IOError:
            print(f"The file {os.path.basename(self.path)} is not a valid image.")

        # this just gets the data which forms the actual image, without metadata
        image_data = image.getdata()

        stripped_image = Image.new(image.mode, image.size)
        stripped_image.putdata(image_data)
        stripped_image.save(
            os.path.join(os.getcwd(), f"{self.name}_stripped.JPEG")
        )


if __name__ == "__main__":
    image = MetadataImage(sys.argv[1])
    print(image.name)
    print("\n")
    print(image.metadata)
    print("\n")
    print(image.GPS_metadata)
    image.save_copy_without_metadata()
