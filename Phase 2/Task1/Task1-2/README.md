# Soccer Ball Detection Documentation

## Overview
This Python script provides a mechanism for detecting blue and red soccer balls in images using OpenCV, NumPy, and Matplotlib. It combines color-based segmentation, morphological operations, and shape analysis to identify soccer balls and outputs detections in YOLO format for further use.

## Techniques Used

1. **Color-Based Segmentation**:
   - **Color Ranges**: Defined HSV ranges for blue and red soccer balls, using multiple ranges per color to handle lighting variations.
   - **Mask Creation**: Masks are generated with `cv2.inRange` to isolate pixels within specified HSV ranges. Masks for each color are combined using `cv2.bitwise_or` to create blue, red, and combined masks.

2. **Morphological Operations**:
   - **Noise Reduction**: An opening operation (`cv2.morphologyEx`, `MORPH_OPEN`) with a 3x3 kernel removes small noise.
   - **Hole Filling**: A closing operation (`MORPH_CLOSE`) with a 7x7 kernel fills gaps in detected regions.
   - **Smoothing**: `cv2.medianBlur` smooths mask boundaries to improve contour detection.

3. **Contour Detection and Shape Analysis**:
   - **Contours**: Extracted using `cv2.findContours` with `RETR_EXTERNAL` mode to focus on outer boundaries.
   - **Filtering**:
     - **Area**: Contours are filtered by area to exclude objects too small or too large relative to image size.
     - **Circularity**: Calculated as \( \text{circularity} = \frac{4 \pi \cdot \text{area}}{\text{perimeter}^2} \), with values between 0.4 and 1.4 indicating circular shapes.
     - **Aspect Ratio**: Bounding rectangle’s width/height ratio is checked (0.6–1.4) for square-like shapes.
     - **Ellipse Fit**: For contours with sufficient points, `cv2.fitEllipse` is used to fit an ellipse, and the area ratio between contour and ellipse confirms circularity.
   - Contours meeting these criteria are classified as soccer balls.

4. **Detection Output**:
   - **YOLO Format**: Bounding boxes are normalized (center x, y, width, height) and saved in YOLO format to text files.
   - **Confidence Score**: Calculated from circularity and area ratio to indicate detection reliability.