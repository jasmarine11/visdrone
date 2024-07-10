import os
import cv2

# Define paths 
# || Edit your directories here! ||
input_image_dir = '/Users/Your_directory'
input_annotation_dir = '/Users/Your_directory'
output_image_dir = '/Users/Your_directory'
output_annotation_dir = '/Users/Your_directory'

# Ensure output directories exist
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_annotation_dir, exist_ok=True)

# Define target size for cropping
target_size = 256

# Adjust the boundary box for the annotations
def adjust_bbox(bbox, crop_x, crop_y, crop_width, crop_height):
    x, y, w, h, score, category, truncation, occlusion = bbox
    new_x = max(x - crop_x, 0)
    new_y = max(y - crop_y, 0)
    new_w = min(w, crop_width - new_x)
    new_h = min(h, crop_height - new_y)
    
    # Filter out bboxes that are completely outside the crop or partially visible
    if new_w <= 0 or new_h <= 0 and new_x + w <= crop_width and new_y + h <= crop_height:
        return None
    
    return [new_x, new_y, new_w, new_h, score, category, truncation, occlusion]

# Crop images and adjust the corresponding annotations
def crop_and_adjust_annotations(image_path, annotation_path, output_image_dir, output_annotation_dir, target_size):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error reading image {image_path}")
        return

    # Get image dimensions (ignore channels)
    height, width, _ = image.shape
    
    # Calculate center points
    center_x, center_y = width // 2, height // 2

    # Calculate the coordinates for the right crop
    x1_right = min(center_x, width - target_size)  # Ensure the right crop stays within image bounds
    y1_right = max(center_y - target_size // 2, 0)  # Ensure the top-left corner doesn't go above the image
    crop_right = image[y1_right:y1_right + target_size, x1_right:x1_right + target_size]
    
    # Calculate the coordinates for the left crop
    x1_left = max(center_x - target_size, 0)  # Ensure the left crop stays within image bounds
    y1_left = max(center_y - target_size // 2, 0)  # Ensure the top-left corner doesn't go above the image
    crop_left = image[y1_left:y1_left + target_size, x1_left:x1_left + target_size]

    # Save the crops with the same base name and appropriate suffix
    base_name = os.path.basename(image_path)
    base_name_no_ext, ext = os.path.splitext(base_name)
    
    output_image_path_right = os.path.join(output_image_dir, f'{base_name_no_ext}_right{ext}')
    output_image_path_left = os.path.join(output_image_dir, f'{base_name_no_ext}_left{ext}')
    
    cv2.imwrite(output_image_path_right, crop_right)
    cv2.imwrite(output_image_path_left, crop_left)
    
    # Load annotations
    annotation_file_path = os.path.join(annotation_path)
    with open(annotation_file_path, 'r') as file:
        annotations = [list(map(int, line.strip().split(','))) for line in file.readlines()]

    # Adjust annotations for right crop
    adjusted_annotations_right = [adjust_bbox(ann, x1_right, y1_right, target_size, target_size) for ann in annotations]
    adjusted_annotations_right = [ann for ann in adjusted_annotations_right if ann is not None]
    
    # Save adjusted annotations for right crop
    output_annotation_path_right = os.path.join(output_annotation_dir, f'{base_name_no_ext}_right.txt')
    with open(output_annotation_path_right, 'w') as file:
        for ann in adjusted_annotations_right:
            file.write(','.join(map(str, ann)) + '\n')
    
    # Adjust annotations for left crop
    adjusted_annotations_left = [adjust_bbox(ann, x1_left, y1_left, target_size, target_size) for ann in annotations]
    adjusted_annotations_left = [ann for ann in adjusted_annotations_left if ann is not None]
    
    # Save adjusted annotations for left crop
    output_annotation_path_left = os.path.join(output_annotation_dir, f'{base_name_no_ext}_left.txt')
    with open(output_annotation_path_left, 'w') as file:
        for ann in adjusted_annotations_left:
            file.write(','.join(map(str, ann)) + '\n')

# Process all images and annotations in the input directories
for image_name in os.listdir(input_image_dir):
    image_path = os.path.join(input_image_dir, image_name)
    annotation_name = image_name.replace('.jpg', '.txt')
    annotation_path = os.path.join(input_annotation_dir, annotation_name)
    
    # Check if the file is an image 
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
        crop_and_adjust_annotations(image_path, annotation_path, output_image_dir, output_annotation_dir, target_size)
    else:
        print(f"Skipping non-image file {image_path}")
