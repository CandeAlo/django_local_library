# Práctica 1

**Autores:** Candela Alonso Fernández, Pablo Tejero Lascorz  
**Pareja:** 04

## Entorno de trabajo

Trabajaremos con Python 3.11 y un entorno virtual en el que instalaremos todas las dependencias requeridas. Se proporciona un listado de las librerías requeridas y sus versiones en el fichero `requirements.txt`.

Para crear y activar el entorno virtual, ejecute:
``` BASH
# Linux
sudo python3.11 -m venv .venv
source .venv/bin/activate
python3.11 -m pip install -r requirements.txt

# Windows
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
py -3.11 -m pip install -r requirements.txt
```

Si ha habido algún error de instalación, consulta el apartado correspondiente al final de este documento.

## Poner en marcha el servidor

Se puede poner en marcha el servidor con el siguiente comando:
``` BASH
# Linux
python3.11 manage.py runserver

# Windows
py -3.11 manage.py runserver
```

Si no funciona, es probable que se deba a que el puerto 8000 (que es el que intentará usar nuestro servidor web de Django) esté ya en uso. Podemos cambiar el puerto a uno que esté disponible (por ejemplo al 8001) simplemente pasándolo como argumento al script:
``` BASH
# Linux
python3.11 manage.py runserver 8001

# Windows
py -3.11 manage.py runserver 8001
```

Una vez el servidor esté en marcha, puedes ver el sitio web navegando a http://127.0.0.1:8001/ en un navegador web local. Recuerda cambiar el puerto si decides usar otro.


## Errores de instalación

Es posible que al instalar las dependencias surgan algunos errores. Se han encontrado dos y sus posibles soluciones:

### Librería `psycopg2`

Es posible que en algunos entornos Linux haya algún error al instalar `psycopg2`. En su lugar, prueba a instalar `psycopg2-binary`.

### Librería `Pillow`

Es posible que en algunos entornos Linux no se pueda instalar `Pillow` porque depende de otras librerías no instaladas. Se puede corregir en sistemas basados en Debian con:
```
sudo apt-get install libjpeg-dev zlib1g-dev
```