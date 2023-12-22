
import json 
import requests


url = "https://ocr.asprise.com/api/v1/receipt"
image = "892.jpg"

res = requests.post(url,data = {'api_k':'TEST','recognizer':'auto','ref_no':'oct_python_123'},
                    files = {'file': open(image,'rb')})

with open("response1.json","w") as f:
    json.dump(json.loads(res.text),f)

### Leer texto e imprimirlo

with open("response1.json","r") as f:
    data = json.load(f)

print(data['receipts'][0]['ocr_text'])

"""
def preprocess_image(image_path):
    import numpy as np
    import cv2
    
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

import json 
import requests
import cv2
import io


url = "https://api.ocr.space/parse/image"
image = "36.jpg"

#img = cv2.imread(image)

#height, width, _ = img.shape
#scale_percent = 2000
#width = int(img.shape[1] * scale_percent / 100)
#height = int(img.shape[0] * scale_percent / 100)
#cv2.resize(img,[width,height], interpolation=cv2.INTER_AREA)

img = preprocess_image(image)

cv2.imwrite('ss.jpg',img)

_, compressedimage = cv2.imencode(".jpg",img,[1, 90])
file_bytes = io.BytesIO(img)

result = requests.post(url,files={image :file_bytes},data={"apikey": "K81927349288957", "language": "eng"})

print(result.content.decode())
"""