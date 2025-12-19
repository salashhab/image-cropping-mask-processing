# Image Cropping and Mask Processing

This repository contains a Python function for cropping a region of interest (ROI) from an image, applying a mask, and analyzing the object in the cropped region. It includes functionalities for calculating dimensions, perimeter, and rotation angle of the cropped object, along with transforming the results into micrometers. The function is useful for image analysis tasks such as object detection, measurement, and manipulation of synthetic images.

## Features

- **Image Cropping**: Crops a specified region of interest (ROI) from an image based on given coordinates.
- **Mask Processing**: Applies a mask to the cropped region to filter out unwanted parts of the image.
- **Object Analysis**: Calculates the dimensions (width, height), perimeter, and rotation angle of the object in the cropped region.
- **Measurement Conversion**: Converts dimensions from pixels to micrometers for accurate physical measurements.
- **Output**: Returns the cropped image with mask applied, along with measurements (in both pixels and micrometers).

## Function Usage

### `process_and_crop_image_with_mask(image_bytes, coordinates=None, mask_data=None, target_size=350)`

#### Parameters:
- `image_bytes` (bytes): The image data in byte format.
- `coordinates` (dict or str, optional): A dictionary or string representing the coordinates of the region to be cropped from the image. If a string, it should be a valid Python dictionary string (e.g., `"{'x': 50, 'y': 100, 'width': 200, 'height': 150}"`).
- `mask_data` (list or array, optional): A list or array representing the mask data used to filter the image. It should be of the same size as the cropped region.
- `target_size` (int, optional): The size (in pixels) to which the resulting image should be scaled. Default is 350 pixels.

#### Returns:
- `image_bytes` (bytes): The processed image in PNG format.
- `texts` (list): A list of calculated values, including:
  - Width (in pixels)
  - Height (in pixels)
  - Width (in micrometers)
  - Height (in micrometers)
  - Perimeter (in pixels)
  - Perimeter (in micrometers)
  - Rotation angle (in degrees)

## Installation

To use this repository, ensure you have the following dependencies installed:

```bash
pip install numpy opencv-python pillow
