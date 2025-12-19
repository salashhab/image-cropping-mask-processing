# Image Cropping and Mask Processing

This repository contains a Python function for cropping a region of interest (ROI) from an image, applying a mask, and analyzing the object in the cropped region. It includes functionalities for calculating dimensions, perimeter, and rotation angle of the cropped object, along with transforming the results into micrometers. The function is useful for image analysis tasks such as object detection, measurement, and manipulation of synthetic images.

## Features

- **Image Cropping**: Crops a specified region of interest (ROI) from an image based on given coordinates.
- **Mask Processing**: Applies a mask to the cropped region to filter out unwanted parts of the image.
- **Object Analysis**: Calculates the dimensions (width, height), perimeter, and rotation angle of the object in the cropped region.
- **Measurement Conversion**: Converts dimensions from pixels to micrometers for accurate physical measurements.
- **Output**: Returns the cropped image with mask applied, along with measurements (in both pixels and micrometers).

## Function Usage

### `process_and_crop_image(image_bytes, coordinates=None, mask_data=None, target_size=350)`

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

### Example Code

Here’s an example of how you can use the `process_and_crop_image_with_mask` function:

```python
from your_repository import process_and_crop_image

# Example inputs
image_bytes = open('your_image.png', 'rb').read()
coordinates = {'x': 50, 'y': 100, 'width': 200, 'height': 150}
mask_data = [0, 1, 0, 1, 1, 0, 0, ...]  # Example mask data (same size as the cropped region)
target_size = 350

# Run the function
processed_image, measurements = process_and_crop_image_with_mask(image_bytes, coordinates, mask_data, target_size)

# Save the processed image
with open('processed_image.png', 'wb') as f:
    f.write(processed_image)

# Print the measurements
for label in ['Width (px)', 'Height (px)', 'Width (µm)', 'Height (µm)', 'Perimeter (px)', 'Perimeter (µm)', 'Angle (°)']:
    print(f"{label}: {measurements.pop(0)}")


```

### Installation

To use this repository, ensure you have the following dependencies installed:

```bash
pip install numpy opencv-python pillow
```

### License

Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) [2025] [Samer Alashhab]

You are free to:
- Share: Copy and redistribute the material in any medium, format, or platform.
- Adapt: Remix, transform, and build upon the material for any purpose, even commercially.
- The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- No additional restrictions: You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Full details at: https://creativecommons.org/licenses/by/4.0/

