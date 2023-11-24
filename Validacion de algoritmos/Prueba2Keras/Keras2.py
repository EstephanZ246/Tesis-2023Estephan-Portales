# Esta programacion fue una prueba para detectar los contornos de los números y realizar recortes a cada uno, al final no se utilizó, 
# porque con Tesseract y Asprise OCR no fue necesario, pero si quieren usarlo para mejorar el rendimiento del algoritmo aquí lo dejo.

import cv2
import numpy as np

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to enhance the text
    threshold_image = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # Perform morphological operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, kernel)
    
    return cleaned_image

def detect_and_crop_numbers(image, min_area=100):
    # Find contours in the preprocessed image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through each contour and crop the numbers
    for i, contour in enumerate(contours):
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate the area of the contour
        contour_area = cv2.contourArea(contour)
        
        # Check if the area is bigger than the minimum area
        if contour_area > min_area:
            # Crop the number from the original image
            number_crop = image[y:y + h, x:x + w]
            
            # Save the cropped number as a new image
            cv2.imwrite(f"number_{i + 1}.png", number_crop)

if __name__ == "__main__":
    # ... (same as before) ...
    input_image_path = 'prueba.jpg'
    
    # Define the minimum area for cropping (you can change this value as desired)
    min_crop_area = 200  # Edit this value as needed
    
    # Preprocess the image
    preprocessed_image = preprocess_image(input_image_path)
    
    # Detect and crop numbers from the preprocessed image
    detect_and_crop_numbers(preprocessed_image, min_area=min_crop_area) 