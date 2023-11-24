
Video explicativo: https://youtu.be/aTcsYL6cX6s


# OPTIMIZACION DE LA HERRAMIENTA DE PROCESAMIENTO DE IMÁGENES PARA EL SISTEMA BRAINLAB DE HUMANA


En este repositorio se encuentran todos los documentos que me fueron útiles para desarrollar mi trabajo de graduación, así como las pruebas independientes que estuve realizando para poder validar las herramientas que se imprementaron en el sistema final de reconocimiento de ángulos de configuración. Entre las validaciones que se realizaron está:

1. Pruebas con protocolo TCP/IP
2. Pruebas con Keras para el reconocimiento de caracteres y machine learning
3. Pruebas con motor de reconocimiento Asprise
4. Pruebas de preprocesamiento de las imágenes

Las programaciones realizadas se encuentran en la carpeta de "Pruebas independientes de programaciones".
Cada una de estas programaciones tiene documentado todos los pasos que se hacen, por lo que para poder comprender qué fue lo que se hizo, es suficiente con dar una lectura a cada una de estas, todas estas funcionan, solo es necesario instalar las librerías necesarias. Para cada una de las programaciones que mencioné, estas son las librerías que se necesitan:

### Pruebas con protocolo TCP/IP

Para ejecutar las programaciones contenidas en esta carpeta son necesarias las siguientes librerías:

- socket
- numpy
- cv2
- time
- datetime
- base64
- sys
- threading

Algunas de estas no son necesarias de instalar nuevamente ya que vienen por defecto con la instalación de python. 

### Prueba2Keras

Para el archivo con nombre "Detection.py" es necesario tener instaladas la siguientes librerías:

- numpy
- matplotlib
- tensorflow

Para el archivo con nombre "Keras2.py" es necesario solamente tener estas librerías:

- cv2
- numpy

Para el archivo con nombre "Prepros2.py" son necesarias las siguientes librerías:

- numpy
- cv2
- pyterreract

### TEST Aspire

En esta carpeta se tiene únicamente una programación que lo que hace es conectarse a un servidor mediante API, mandar una imagen para ser procesada, luego se recibe un archivo JSON con la información procesada, debido a esto solamente es necesario de 2 librerías las cuales son:

- json
- requests

## Archivos de ayuda

En las carpetas con nombre "Documentación" e "Investigación" se encuentran algunos documentos que dan mucha información útil para todo lo que involucra el proyecto, más que todo el procesamiento que se le puede realizar a las imágenes previo a realizar el reconocimiento de los caracteres. Algunos documentos como el "PROCESAMIENTO DE IMAGENES.pdf" dan mucha información utilizando la librería de la cuál se hace mucho uso durante el proyecto, esta es opencv utilizado en una Raspberry PI. Los otros documentos dan una buena guía de los mejores procesos que se pueden llevar a cabo en el procesamiento de las imágenes.

## Prototipo final de proyecto

Esta carpeta contiene el prototipo del proyecto, el proyecto se divide en 3 archivos de los cuales 2 pertenecen al cliente y 1 al servidor. Estos son:
### Cliente
- Cliente.py
- GUI.py
- Functions.py
### Servidor
- Server.py
- Functions.py

El cliente está pensado para ejecutarse en una computadora convencional, y para ejecutarse necesita que se tengan las siguientes librerías:

- Tkinter
- ttkthemes
- PIL
- socket
- numpy
- cv2
- time
- datetime
- base64
- sys
- pyautogui
- pytesseract
- serial

El servidor en cambio, está pensado para poder ejecutarse tanto en computadora convencional y en un sistema embebido, las librerías que se necesitan para poder ejecutarse son:

- socket
- numpy
- threading
- cv2
- time
- datetime
- base64
- pytesseract
- numpy

Tanto el cliente como el servidor dependen del archivo "functions.py" por lo que será necesario instalar las librerías a las que functions tiene dependencia.

En todos los archivos se encuentra una buena descripción de para qué sirve y qué realiza cada algoritmo implementado en cada uno.

# Validacion de algoritmos

En esta carpeta se encuentran algunos archivos de los algoritmos implementados en la interfaz. 
