# UIGeneration
This project aims to generate hand-drawn website pages by combining single UI elements.

## File Structure
Elements: Folder containing subfolders with image files (e.g., button, navbar, profile, text). Can replace the elements with data we collected from user studies. \
formats: Folder containing JSON configuration files for image layout (.json). Each page will be generated randomly based on the formats. \
output: Folder where the final combined image will be saved. \
main.py: The Python script that runs the image-generating process.

## Configuration
canvas_size: Defines the width and height of the canvas (in pixels). \
layers: A list of layers where each layer corresponds to a folder of images. \
Each layer can have:
  - folder: the folder containing images for the layer (e.g., button, navbar).
  - repeat_range: the minimum and maximum number of images to randomly repeat in this layer.
  - resize: defines the new size of images in this layer.
  - position: the final position of the element
  - random_position: if true, images will be placed randomly on the canvas.

## Running the Script
```
python main.py
```
