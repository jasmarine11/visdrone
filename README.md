# visdrone
# VisDrone2019 Image Cropping and Annotation Adjustment

This project focuses on processing the VisDrone2019 dataset for object detection. It involves cropping large images into smaller, standardized sizes and adjusting the corresponding bounding box annotations accordingly.

## Project Description

Drones equipped with cameras have been deployed in various applications such as agriculture, aerial photography, delivery, and surveillance. The VisDrone2019 dataset provides a large-scale benchmark for computer vision tasks, particularly object detection. This project aims to preprocess this dataset by cropping the images and adjusting the annotations to fit the cropped images. Ultimately, we aim to develop a robust object detection model using the YOLO architecture to accurately identify and categorize objects such as people, bicycles, and cars within the images. Our final deliverables will include a trained YOLO model, a comprehensive summary report, and a presentation detailing our methodology and results.

## Dataset

The VisDrone2019 dataset consists of:
- 6,471 training images
- 548 validation images
- 1,580 test-challenge images

Each image has an accompanying annotation file containing bounding box information for objects within the image.

## Objectives

1. **Crop Images**: Each image is cropped into two 256x256 images.
2. **Adjust Annotations**: Update the bounding box coordinates in the annotations to match the cropped images.
3. **Include Only Fully Visible Objects**: Ensure only objects fully visible within the cropped area are included in the annotations.

## Usage

1. **Define Input and Output Paths**:
    - `input_image_dir`: Path to the directory containing original images.
    - `input_annotation_dir`: Path to the directory containing original annotation files.
    - `output_image_dir`: Path to the directory where cropped images will be saved.
    - `output_annotation_dir`: Path to the directory where updated annotation files will be saved.

2. **Run the Script**:
    ```bash
    python crop_and_adjust_annotations.py
    ```

## Progress Updates

### Completed Tasks
- Downloaded and organized the VisDrone2019 dataset.
- Implemented image cropping to create two 256x256 crops from each image.
- Adjusted annotations to ensure they align with the cropped images.
- Included only fully visible objects in the annotations for simplicity.
- Review and summarize relevant research papers to determine the best model for training.

### Next Steps
- Implement a YOLO model to train on the processed dataset.
- Validate the model and fine-tune as needed.
