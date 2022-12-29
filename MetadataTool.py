import os
import sys

from MetadataImage import MetadataImage


class MetadataTool:
    def __init__(self, input_path) -> None:
        self._input_path = input_path
        self.images_to_process = []

    @property
    def input(self):
        if os.path.isdir(self._input_path):
            pass
    pass

    def prepare_images(self):
        if os.path.isfile(self._input_path):
            self.images_to_process.append(self._input_path)

        if os.path.isdir(self._input_path):
            # https://stackoverflow.com/questions/71112986/retrieve-a-list-of-supported-read-file-extensions-formats
            pass


if __name__ == "__main__":
    # WIP
    image = MetadataImage(sys.argv[1])
    print(image.name)
    print("\n")
    print(image.metadata)
    print("\n")
    print(image.GPS_metadata)
    image.save_copy_without_metadata()
