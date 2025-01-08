# image-metadata-tool
A small tool for viewing and stripping image metadata.

## Installation

Clone the repository, set up a virtual environment and install the requirements to it (`pip install -r requirements.txt`).

## Usage

The tool is a work in progress, but a basic use case of creating a metadata-stripped copy of a single image is supported. To do so, run `MetadataTool.py` and pass the path to the image you'd like to create a copy of:

```python MetadataTool.py path/to/image.jpg```

You should see the image metadata printed into your console, and a new image should be created, named after your source image, with `_stripped` appended at the end. As the name suggests, this copy should be stripped of metadata.

**Note!** Currently the process strips ALL metadata, which includes the color profile. As a result, the stripped copy can have slightly flatter colors than the original. I'll try to make the stripping process more granular in the future.

### Supported formats
The tool supports the same image formats as `Pillow` library: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
