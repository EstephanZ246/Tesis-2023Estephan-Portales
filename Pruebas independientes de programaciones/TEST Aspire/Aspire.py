
# Esta programación es para utilizar Asprise para identificar el texto.
# Esto es lo único necesario para utilizarlo, considerar que solo se tienen como 5 
# intentos por ip cada cierto tiempo ya que la API usada es una prueba gratuita, la 
# versión completa tiene un costo como de 300 dolares al mes, sin embargo, es la que 
# mejores resultados dió. Solo la puse en el proyecto como una alternativa al uso 
# de tesseract en caso se quiera pagar.

# En la carpeta Joint1, Joint2 y Joint3 están los recortes que se hacen a la imágenes que se obtienen del 
# programa Brainlab que se usa en HUMANA


import json 
import requests

# Aquí se da el url de donde se direcciona la API y el directorio de la imagen que se quiere reconocer.
# el resultado se genera en un JSON que se almacena en la raiz de la carpeta actual y luego solo se imprime 
# en consola el resultado del texto identificado
url = "https://ocr.asprise.com/api/v1/receipt"
image = "892.jpg"

res = requests.post(url,data = {'api_k':'TEST','recognizer':'auto','ref_no':'oct_python_123'},
                    files = {'file': open(image,'rb')})

with open("response1.json","w") as f:
    json.dump(json.loads(res.text),f)

### Leer texto e imprimirlo
# En caso se quiere ver todo lo que la API devuelve, solo imprimir la variable data

with open("response1.json","r") as f:
    data = json.load(f)

print(data['receipts'][0]['ocr_text'])

