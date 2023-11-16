import os
import cv2
import numpy as np
from skimage.feature.texture import graycomatrix, graycoprops
from rembg import remove
from PIL import Image
import joblib
import pandas as pd

model = joblib.load('assets/training/trained_model-2.joblib')

def extract_texture_features(image):
    # Convert the original image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sobel edge detection
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate gradient magnitude and direction
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    gradient_direction = np.arctan2(sobel_y, sobel_x)

    # Calculate GLCM (Gray-Level Co-occurrence Matrix) for the original grayscale image
    glcm = graycomatrix(gray, [1], [0], symmetric=True, normed=True)

    # Calculate GLCM properties for the original grayscale image
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]

    avg_color = np.mean(image, axis=(0, 1))

    return [avg_color[0], avg_color[1], avg_color[2], contrast, correlation, energy, homogeneity]

# Folder path containing the images
image_folder_path = 'assets/training/image/retak'

# List to store the results
results = []

# Iterate through each image in the folder
for filename in os.listdir(image_folder_path):
    if filename.endswith(".jpg"):
        # Load the image
        image_path = os.path.join(image_folder_path, filename)
        image = cv2.imread(image_path)
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        removed_bg_image = remove(pil_image).convert("RGB")
        removed_bg_image = np.array(removed_bg_image)

        # Extract texture features
        texture_features = extract_texture_features(removed_bg_image)

        # Predict the category
        predicted_category = model.predict([texture_features])

        # Append the result to the list
        result = {
            'Image': filename,
            'Predicted Category': predicted_category[0]
        }
        results.append(result)

# # Create a DataFrame from the results list
# df = pd.DataFrame(results)

# # Save the DataFrame to an Excel file
# excel_file_path = 'result_telur.xlsx'
# df.to_excel(excel_file_path, index=False)
# print(f"Results saved to {excel_file_path}")
