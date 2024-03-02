from json import JSONEncoder
import json
import cv2
import numpy as np
import joblib
from skimage.feature.texture import graycomatrix, graycoprops
from PIL import Image
from rembg import remove
from utils import WebResponseData
from model import connected_user_client


class ImageProccesingService():

    def extract_texture_features(self, image):
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

    def EggCrackDetection(self, image_test):
        model = joblib.load('assets/trained_model-2.joblib')
        # test_image_path = 'TEST/test2.jpg'
        path_image = f"assets/image/{image_test}"
        test_image = cv2.imread(path_image)
        pil_test_image = Image.fromarray(
            cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        removed_bg_test_image = remove(pil_test_image).convert("RGB")
        removed_bg_test_image = np.array(removed_bg_test_image)

        # Extract texture features using GLCM, grayscale, and Sobel edge detection
        texture_features = self.extract_texture_features(removed_bg_test_image)

        # Predict the category of the detected object using the trained model
        predicted_category = model.predict([texture_features])

        # Print messages based on the predicted category
        if predicted_category[0] == 'retak':
            data_result = {
                "condition": True,
                "message": "Telur sudah retak"
            }

            event_message_data = {
                "event": "new_message",
                "id": "message_id",
                "retry": 15000,
                "data": data_result}
            self.sendToUser(json.dumps(event_message_data))
            return WebResponseData(data=data_result)
        else:
            return WebResponseData(data={
                "condition": False,
                "message": "Telur tidak retak"
            })

    def sendToUser(self, message):
        user_id = "oukenze"
        if user_id in connected_user_client:
            _, client_queue = connected_user_client[user_id]
            client_queue.put_nowait(message)
