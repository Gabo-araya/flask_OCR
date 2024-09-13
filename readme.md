![[header_keyboard.jpg]]
# Flask OCR

---
Tags:  #codigo #linux #readme #python

> [!info] Volver a [[Home]]

---

## 1. Pre-requisitos

_Esta es una lista de los paquetes que deben estar instalados previamente:_

* **Python 3**
	- [Ayuda - https://docs.microsoft.com/en-us/windows/python/beginners)](https://docs.microsoft.com/en-us/windows/python/beginners)
	- [Curso Django desde Cero en youtube](https://www.youtube.com/watch?v=vo4VF3neyrs)
	- [Video del proyecto por Dennis Ivy](https://www.youtube.com/watch?v=llbtoQTt4qw)

* **Pip**
	- [Ayuda - https://tecnonucleous.com/2018/01/28/como-instalar-pip-para-python-en-windows-mac-y-linux/](https://tecnonucleous.com/2018/01/28/como-instalar-pip-para-python-en-windows-mac-y-linux/)

* **Virtualenv**
	- [Ayuda - https://techexpert.tips/es/windows-es/instalacion-del-entorno-virtual-de-python-en-windows/](https://techexpert.tips/es/windows-es/instalacion-del-entorno-virtual-de-python-en-windows/)

---
## 2. Preparar ambiente de trabajo

### Instalación pre-requisitos [Windows] 🔧

Muchas veces tenemos ese problema común de no poder instalar ciertas librerías o realizar configuraciones para poder desarrollar en Windows para Web y es por ello que en éste tutorial vamos a ver los pasos para instalar Python y configurarlo con Pip y Virtualenv para así poder empezar a desarrollar aplicaciones basadas en éste lenguaje e instalar Django para crear aplicaciones web. [Ver video -> **https://www.youtube.com/watch?v=sG7Q-r_SZhA**](https://www.youtube.com/watch?v=sG7Q-r_SZhA)

1. Descargamos e instalamos Python 3.6 (o una versión superior) para Windows

    - [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Agregaremos Python a las variables de entorno de nuestro sistema si es que no se agregaron durante la instalación para que así podamos ejecutarlo desde la terminal `/cmd`

    - `C:\Python34 y C:\Python34\Scripts`
3. Ejecutamos Pip para verificar que esté instalado correctamente

    - `pip --version`
4. Instalamos Virtualenv con pip

    - `pip install virtualenv`
5. Verificamos la versión de Virtualenv

    - `virtualenv --version`
6. Crearemos un entorno virtual con Python

    - `virtualenv test`
7. Iniciamos el entorno virtual

    - `.\test\Scripts\activate`
8. Finalmente desactivamos el entorno virtual

    - `deactivate`

### Instalación pre-requisitos [GNU/Linux] 🔧

1. Ejecutamos Pip para verificar que esté instalado correctamente

    - `pip3 --version`
2. Instalamos Virtualenv con pip

    - `pip3 install virtualenv`
3. Verificamos la versión de Virtualenv

    - `virtualenv --version`
4. Crearemos un entorno virtual con Python

    - `python3 -m venv ./env`
5. Activamos el entorno virtual

    - `source ./env/bin/activate`

```
source ./env/bin/activate
```

6. Finalmente desactivamos el entorno virtual

    - `deactivate`

---
## 3. Comandos para instalación y configuración de paquetes

### 3.1 Configuración de entorno local

* Revisar versión de python. Linux puede tener más de una versión de python instalada.
```
$ python3 --version
$ python --version // versión de python 2
```

* Instalacion de pip
`pip` es un sistema de gestión de paquetes utilizado para instalar y administrar paquetes de software escritos en Python. Para instalar paquetes pip en Python 3 se debe utilizar el comando `pip3`.
```
$ sudo apt install python3-pip
```

* Instalación de virtualenv
Video de apoyo: [Entornos Virituales (virtualenv) de Python en Visual Studio Code](https://www.youtube.com/watch?v=2kLYOzNb3uU)

![https://www.youtube.com/watch?v=2kLYOzNb3uU](https://www.youtube.com/watch?v=2kLYOzNb3uU)

```
pip3 install virtualenv
```

```
virtualenv --version
```

A veces también se necesita instalar el venv en python3

```
sudo apt-get install python3-venv
```

### 3.2 Entorno virtual e instalación de paquetes

Por orden, es ideal que los entornos virtuales se guarden todos en el mismo lugar. Aunque algunos prefieren que vaya junto con cada proyecto. Para gustos, colores.

* Crear entorno virtual

```
cd /home/gabo/envs/
```

Este comando creará un entorno virtual llamado `env` en el directorio `~/envs/usuario/`
```
python3 -m venv /home/gabo/envs/proyecto/env
```


Si ya estás en la carpeta donde se guardarán los entornos virtuales:
```
python3 -m venv env
```

![[django_virtualenv.png]]

* Activar entorno virtual
```
source env/bin/activate
```

```
source ~/envs/proyecto/venv/bin/activate
```

```
source /home/gabo/pyscripts/venv/bin/activate
```

* Para desactivar el entorno virtual y volver al entorno global se usa este comando:

```
(env) $ deactivate
```

* Congelar los paquetes instalados en el env
```
pip3 freeze > requirements.txt
```

* Instalar los requerimientos
```
python3 -m pip install -r requirements.txt
```

* Instalación de paquetes
```
pip3 install Flask Pillow pytesseract requests exifread
```

```
pip3 install flask-session flask-wtf flask-talisman bcrypt python-dotenv python-magic cryptography
```


Para instalar una versión específica de un paquete
```
pip3 install openpyxl==3.1.5
```


* Pillow: Para manipular imágenes.
* pytesseract: Para realizar el reconocimiento óptico de caracteres (OCR).

## 4. Creación de script

Se realizará scraping sobre la página
* https://books.toscrape.com/index.html
* https://books.toscrape.com/catalogue/page-1.html

```Python
# flaskOCR.py

from flask import Flask, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Guardar la imagen temporalmente
            file.save('temp.jpg')
            # Realizar OCR
            text = pytesseract.image_to_string(Image.open('temp.jpg'))
            return text
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

```


## 5. Plantilla HTML (index.html)

``` HTML
<!DOCTYPE html>
<html>
<head>
    <title>OCR Image Uploader</title>
</head>
<body>
    <h1>Sube una imagen para OCR</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Subir y Procesar">
    </form>
</body>
</html>
```

---

## 6. Explicación

- **Ruta raíz:** La ruta `'/'` maneja tanto las solicitudes GET (mostrar el formulario) como POST (procesar la imagen).
- **Subida de archivos:** Se utiliza `request.files` para acceder al archivo subido.
- **Guardar imagen:** Se guarda la imagen temporalmente en un archivo con nombre 'temp.jpg'.
- **Realizar OCR:** Se utiliza `pytesseract.image_to_string` para extraer el texto de la imagen.
- **Mostrar resultado:** Se devuelve el texto extraído como respuesta.

**Consideraciones adicionales:**

- **Seguridad:**
    - Limita los tipos de archivos permitidos para evitar ataques de subida de archivos.
    - Limita el tamaño máximo de los archivos.
- **Precisión de OCR:** La precisión de OCR depende de la calidad de la imagen y la configuración de pytesseract.
- **Mejoras:**
    - **Interfaz de usuario:** Personaliza la apariencia y funcionalidad del formulario.
    - **Procesamiento en segundo plano:** Utiliza tareas asíncronas para no bloquear el servidor mientras se procesa la imagen.
    - **Almacenamiento de imágenes:** Considera almacenar las imágenes en un sistema de almacenamiento en la nube.
    - **Preprocesamiento de imágenes:** Mejora la calidad de la imagen antes de realizar el OCR.
- **Integración con otros servicios:** Puedes integrar este sistema con servicios de reconocimiento de texto más avanzados o con servicios de almacenamiento en la nube.

## 7. Ejemplo completo con mejoras

``` python
# ... (código anterior)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ... (validaciones y procesamiento)
        # ... (guardar imagen en la nube, si es necesario)
        text = pytesseract.image_to_string(Image.open('temp.jpg'), lang='eng')  # Especificar idioma
        return render_template('result.html', text=text)

# Plantilla result.html
<!DOCTYPE html>
<html>
<head>
    <title>Resultado OCR</title>
</head>
<body>
    <h1>Texto extraído:</h1>
    <p>{{ text }}</p>
    <a href="/">Subir otra imagen</a>
</body>
</html>
```



**Próximos pasos:**

- **Personalización:** Adapta el código a tus necesidades específicas.
- **Mejoras:** Implementa las mejoras mencionadas anteriormente.
- **Pruebas:** Realiza pruebas exhaustivas con diferentes tipos de imágenes.

**Recursos adicionales:**

- **Documentación de Flask:** [https://flask.palletsprojects.com/en/2.2.x/](https://flask.palletsprojects.com/en/2.2.x/)
- **Documentación de Pillow:** [https://pillow.readthedocs.io/en/stable/](https://pillow.readthedocs.io/en/stable/)
- **Documentación de pytesseract:** [https://pypi.org/project/pytesseract/](https://pypi.org/project/pytesseract/)

---
## 8. Ejecutar la aplicación Flask

**¡Excelente!** Ya tienes la estructura básica de tu aplicación Flask para realizar OCR. Ahora, para ponerla en funcionamiento, necesitarás ejecutar el archivo Python que contiene tu código.

### 1. **Abre tu terminal o línea de comandos.**

- **Navega hasta el directorio** donde se encuentra tu archivo Python (por ejemplo, `app.py`).

### 2. **Ejecuta el siguiente comando:**

Bash

```
flask run
```

O, si prefieres usar el módulo `flask` directamente:

Bash

```
python -m flask
```

### 3. **Accede a la aplicación:**

Una vez que el servidor se inicie, se te proporcionará una URL (por ejemplo, `http://127.0.0.1:5000/`). Abre esta URL en tu navegador para acceder a tu aplicación.

### **Opciones adicionales:**

- **Especificar el archivo:** Si tu archivo no se llama `app.py` o `wsgi.py`, puedes especificarlo así:

    Bash

    ```
    flask run --app tu_archivo.py
    ```

- **Cambiar el puerto:**

    Bash

    ```
    flask run --host=0.0.0.0 --port=8080
    ```

    Esto te permitirá acceder a la aplicación desde otras máquinas en la red, utilizando el puerto 8080.
- **Modo depuración:** El modo depuración te permite recargar automáticamente la aplicación cuando haces cambios en el código y proporciona un depurador interactivo. Para activarlo:

    Bash

    ```
    set FLASK_ENV=development
    flask run
    ```

    (En Windows) o

    Bash

    ```
    export FLASK_ENV=development
    flask run
    ```

    (en Linux/macOS)

### **Consideraciones adicionales:**

- **Virtual environments:** Si estás utilizando un entorno virtual, asegúrate de activarlo antes de ejecutar el comando `flask run`.
- **Seguridad:** Al desarrollar en modo depuración, asegúrate de que tu aplicación no esté expuesta a internet directamente.
- **Producción:** Para desplegar tu aplicación en producción, necesitarás un servidor web como Gunicorn o uWSGI, y un servidor de aplicaciones como Apache o Nginx.

**Ejemplo completo (en Linux/macOS):**

Bash

```
# Activar el entorno virtual (si lo estás usando)
source ./env/bin/activate

# Navegar al directorio de la aplicación
cd mi_proyecto_flask

# Ejecutar la aplicación en modo desarrollo
export FLASK_ENV=development
flask run
```

**¡Con esto, deberías poder ejecutar tu aplicación Flask y comenzar a subir imágenes para realizar OCR!**

**¿Tienes alguna otra pregunta sobre cómo ejecutar tu aplicación o sobre alguna parte del código?**

**Consejos adicionales:**

- **Explora la documentación oficial de Flask:** [https://flask.palletsprojects.com/en/2.2.x/](https://flask.palletsprojects.com/en/2.2.x/)
- **Utiliza herramientas de desarrollo:** Los IDEs como PyCharm o Visual Studio Code ofrecen herramientas para depurar y perfilar tu aplicación Flask.
- **Considera utilizar un framework de despliegue:** Heroku, AWS Elastic Beanstalk o Google Cloud Platform son opciones populares para desplegar aplicaciones Flask.

**¿Qué más te gustaría saber sobre Flask o sobre el desarrollo web en general?**
