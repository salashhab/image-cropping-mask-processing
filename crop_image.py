import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import ast


def image_to_bytes(img):
    buf = BytesIO()
    Image.fromarray(img.astype(np.uint8)).save(buf, format="PNG")
    return buf.getvalue()

def process_and_crop_image_with_mask(image_bytes, coordinates=None, mask_data=None, target_size=350): 
    # Open image and convert to numpy array
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = np.array(image)
    
    # Parse coordinates
    if isinstance(coordinates, str):
        coordinates_dict = ast.literal_eval(coordinates)
    else:
        coordinates_dict = coordinates

    x = coordinates_dict['x']
    y = coordinates_dict['y']
    width = coordinates_dict['width']
    height = coordinates_dict['height']

    # Crop region of interest
    region_of_interest = image[y:y+height, x:x+width]

    # Process mask
    expected_size = height * width 
    corrected_mask_data = mask_data[:expected_size]
    mask_array = np.array([int(c) for c in corrected_mask_data]).reshape((height, width)).astype(np.uint8)
    mask_uint8 = (mask_array * 255).astype(np.uint8)
    masked_region = cv2.bitwise_and(region_of_interest, region_of_interest, mask=mask_uint8)

    # Convert to grayscale and remove background noise
    gray = cv2.cvtColor(masked_region, cv2.COLOR_BGR2GRAY)
    tolerance = 40
    background_gray = 200
    mask = cv2.inRange(gray, background_gray - tolerance, background_gray + tolerance)
    foreground_mask = cv2.bitwise_not(mask)
    gray_cleaned = cv2.bitwise_and(gray, gray, mask=foreground_mask)

    # Threshold the image to binary and find contours
    _, thresh = cv2.threshold(gray_cleaned, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        # Try again with a different tolerance
        tolerance = 10
        background_gray = 0
        mask = cv2.inRange(gray, background_gray - tolerance, background_gray + tolerance)
        foreground_mask = cv2.bitwise_not(mask)
        gray_cleaned = cv2.bitwise_and(gray, gray, mask=foreground_mask)
        _, thresh = cv2.threshold(gray_cleaned, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours found, return default text
    if not contours:
        texts = ["0", "0", "0", "0", "0", "0", "0"]
        return image_to_bytes(gray_cleaned), texts

    # Flatten contours and get rotated rectangle
    all_points = np.vstack(contours)
    rotated_rect = cv2.minAreaRect(all_points)
    box_points = cv2.boxPoints(rotated_rect)
    box_points = np.intp(box_points)

    # Find contours from the mask and calculate perimeter
    contours2, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_contour = max(contours2, key=cv2.contourArea)
    perimeter_px = cv2.arcLength(largest_contour, True)  

    # Extract dimensions and angle
    (width, height) = rotated_rect[1]
    angle = rotated_rect[2]

    # Create a black 350x350 background and center the masked region
    black_background = np.zeros((target_size, target_size, 3), dtype=np.uint8)

    # Ensure the region fits inside the target size
    if height > target_size or width > target_size:
        scale = min(target_size / width, target_size / height)
        masked_region = cv2.resize(masked_region, (int(width * scale), int(height * scale)))
        height, width = masked_region.shape[:2]

    y_offset = (target_size - height) // 2
    x_offset = (target_size - width) // 2
    black_background[y_offset:y_offset + height, x_offset:x_offset + width] = masked_region

    # Convert to micrometers and calculate perimeter in micrometers
    width_micrometer = width * 40 / 1280 * 10.0
    hieght_micrometer = height * 40 / 960 * 10.0
    
    if width > 0:
        pixel_size_µm = width_micrometer / width
        perimeter_µm = perimeter_px * pixel_size_µm
    else:
        pixel_size_µm = 0
        perimeter_µm = 0

    # Prepare text
    texts = [
        f" {width:.2f}",
        f" {height:.2f}",
        f" {width_micrometer:.2f}",
        f" {hieght_micrometer:.2f}",
        f" {perimeter_px:.2f}",
        f" {perimeter_µm:.2f}",
        f" {angle:.2f}"
    ]
    
    # Save result to PNG and return bytes
    result_image = Image.fromarray(black_background.astype(np.uint8))
    buffer = BytesIO()
    if width > 0 and height > 0:
        result_image.save(buffer, format="PNG")
    
    return buffer.getvalue(), texts
