# Esta fue una prueba para realizar el aumento de las imágenes y reconocer el texto con Tesseract. Este 
# algoritmo sí se utiliza en la versión final del prototipo.

import numpy as np
import cv2
import pytesseract

# Esta funcion realiza el aumento de la imagen y aplica un preprocesamiento a la imagen para que Tesseract pueda reconocerlo un poco mejor
# se puede tunear el scale_percent para que se mejore el reconocimiento, lo que mejor me funcionó fue usar de 2000 a 20000. En ese rango 
# se dieron los mejores resultados. 

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    scale_percent = 2000 
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
  
# resize image
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    threshold_image = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    
    
    return cleaned_image

# Aquí se le dice a Tesseract donde está instalado, solo es necesario en windows,
# en versiones de linux no se necesita, solo intalar el pytesseract con pip


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Aquí se escoge la imagen a trabajar y se reconoce. Whitelist es para que solo reconozca los dígitos o caracteres dentro de las comillas.
input_image_path = 'AnguloJoint1.jpg'

im = preprocess_image(input_image_path)


whitelist = '0123456789.°-+'
Texto_joint = pytesseract.image_to_string(im, config=f'--psm 6 -c tessedit_char_whitelist={whitelist}')
Texto_joint = float(Texto_joint)
print(Texto_joint)

# Se muestra la imagen
cv2.imshow('ppp',im)
cv2.waitKey(0)

