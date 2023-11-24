# Resultado de prototipo final 

El proyecto consta de 2 partes, la primera es el cliente el cuál se encarga de las siguientes tareas:

- Conectar con sistema robótico y mandarle información de ángulos de configuración.
- Realizar captura de la ventana del sistema de Brainlab.
- Vista preliminar de captura de pantalla.
- Mandar el screenshot tomado al servidor 
- Conectarse con servidor en sistema embebido.
- Visualizar los ángulos reconocidos.

El servidor no tienen una interfaz, sino este se ejecuta en consola, al ejecutarse en consola, esta imprime un mensaje que indica que el servidor está funcionando, así mismo, se imprime la IP y puerto al que se puede conectar desde el cliente para poder enviarle los datos.

En esta sección se encuentran 2 carpetas. La primera carpeta tiene como nombre "Prototipo V1", en este se tiene el protoipo que funciona con las imágenes proporcionadas por el trabajo de graduación anterior. Y en "Prototipo V2" se tienen las versiones que funcionan con las imágenes que se tomaron más recientemente, Noviembre 2023.

Ambas versiones contienen el mismo protocolo desarrollado para el sistema robótico. 

La carpeta V1 tiene las siguientes carpetas:
- Sistema Robótico:
- Versión Sistema Embebido Asp.
- Versión Sistema Embebido Te.
- Versión Sistema Todo en uno Asp.
- Versión Sistema Todo en uno Te.

Las abreviaciones Asp  y Te corresponden a Asprise y Tesseract respectivamente, esto quiere decir que una versión implementa el motor de Asprise y el otro el Tesseract. 

La versión de Asprise necesita conexión a internet para funcionar, esto ya que se conecta mediante API. En cambio, Tesseract, la versión todo incluido no necesita de conexión a internet, únicamente haber instalado las librerías correspondientes.

La carpeta V2 contiene lo mismo que la versión V1, con la excepción de las siguientes carpetas:
- Imagenes
- Versiones Modificadas para Raspberry

Esta versión "Modificadas para Raspberry" contienen lo mismo que la versión del servidor remoto, pero omite algunas líneas de código para poder ejecutarse correctamente en la versión de Raspbian.


