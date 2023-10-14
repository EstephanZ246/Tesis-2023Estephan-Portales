# Este archivos es un prototipo para crear un modelo con machine learning para realizar el recorte a las imágenes, este realmente
# no se utiliza en el proyecto porque no es necesario realizar un modelo que posiblemente cargue el CPU del sistema embebido
# cuando no es necesario porque lo recorte siempre se hacen en el mismo lugar. Pero si para fases posteriores les sirve, ahí lo dejo.


import os
import numpy as np
from PIL import Image
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
import cv2
from FuncionesPrePro1 import *
import pytesseract
import numpy as np
from matplotlib import pyplot
from matplotlib import rcParams

# Se toma la imagen que se quiere trabajar
image_file= os.path.dirname(os.path.realpath(__file__)) + "\\Capturas\\"
print(image_file)

# Esta parte está comentada, pero para usarla solo se descomenta el bloque, esta parte es para crear el modelo de machine learning.
"""

# Load and preprocess the images (similar to the previous example)
image_paths = [image_file+'Foto1.jpg', image_file+'Foto2.jpg', image_file+'Foto3.jpg',image_file+'Foto4.jpg',image_file+'Foto5.jpg',image_file+'Foto6.jpg',image_file+'Foto7.jpg']#,Foto8.jpg,Foto9.jpg,Foto10,jpg
images = []
dim = []
for image_path in image_paths:
    image = Image.open(image_path)

    widthim,heightim = image.size
    dim.append([widthim,heightim])

    image = image.resize((224, 224))  # Resize the image to a consistent size
    image = np.array(image) / 255.0  # Normalize pixel values
    images.append(image)


# Define the model (similar to the previous example)

model = Sequential()
model.add(Flatten(input_shape=(224, 224, 3)))
model.add(Dense(64, activation='relu'))
model.add(Dense(4))  # Output layer for bounding box coordinates (x, y, w, h)

# Compile and train the model (similar to the previous example)
model.compile(optimizer=Adam(), loss='mean_squared_error')
X_train = np.array(images)
new_width = 224
new_height = 224
recortes = ([[345,61,515,75], [360,60,515,83], [344,44,517,75], [336,46,515,80], [339,45,524,77], [158,20,223,32], [110,13,228,33]])
# Redimencionar recortes a nueva escala 244x244
contador = 0
for i in dim:
    original_width = i[0]
    original_height = i[1]

    recortes_temporales = recortes[contador]
    recortes_temporales[0] = np.round(recortes_temporales[0]*new_width/original_width)
    recortes_temporales[1] = np.round(recortes_temporales[1]*new_height/original_height)
    recortes_temporales[2] = np.round(recortes_temporales[2]*new_width/original_width)
    recortes_temporales[3] = np.round(recortes_temporales[3]*new_height/original_height)
    recortes[contador] = recortes_temporales
    contador  = contador + 1
    

y_train = np.array(recortes)
history = model.fit(X_train, y_train, epochs=500, batch_size=1)
# Save the model
model.save('model.h5')


"""


#"""
# Aquí ya se usa el modelo de machine learning para hacer el recorte en alguna otra foto que deseemos

# Load the saved model for future prediction
loaded_model = load_model('model.h5')

# Predict bounding box coordinates for a new image
new_image_path = image_file + 'Foto4.jpg'
new_image = Image.open(new_image_path)
new_image = new_image.resize((224, 224))
new_image = np.array(new_image) / 255.0

X_test = np.array([new_image])
y_pred = loaded_model.predict(X_test)

# Extract bounding box coordinates (similar to the previous example)
x, y, w, h = y_pred[0]

# Ensure the coordinates are within valid range
x = max(0, min(x, new_image.shape[1] - 1))
y = max(0, min(y, new_image.shape[0] - 1))
w = max(1, min(w, new_image.shape[1] - x))
h = max(1, min(h, new_image.shape[0] - y))

# Crop the image using the adjusted bounding box coordinates
cropped_image = new_image[int(y):int(y + h), int(x):int(x + w), :]

# Display the cropped image (similar to the previous example)
cropped_image = Image.fromarray(np.uint8(cropped_image * 255.0))
#cropped_image.show()

# Guardar imagen cortada

cropped_image.save(os.path.dirname(os.path.realpath(__file__)) + '\RecortesPrueba\Recorte.jpg')

# Hacer reconocimiento de Joint con Tesseract

img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '\RecortesPrueba\Recorte.jpg')


# Esta parte está comentada, para usarla solo de descomenta. Sirve para realizar el reconocimiento del texto al recorte que se hace con el modelo 
# en el bloque anterior.

#"""

#"""
#resized_image = cv2.resize(img, (244, 68))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ocr_result= pytesseract.image_to_string(img)
print(ocr_result[0:7])


cv2.imshow('1',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
#"""