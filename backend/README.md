# SPORTER Product API

Este es el módulo backend para el primer proyecto de Prácticas Profesionalizantes 3 del IES 9012 en Informática. El proyecto consta de la elaboración de un catálogo de productos.

Los integrantes del grupo son:

- Andrade, Mauro
- Ramirez, Yhonny
- Rinaldi, Germán
- Rogriguez, Martin

## Guía de Setup

Para instalar Sporter API en tu sistema de manera directa, procede a [Instalacion en tu sistema](#instalación-en-tu-sistema), si decides ir por el camino Docker entonces a [Despliegue con Docker](#despliegue-con-docker).

Antes de proceder con cualquiera de estas opciones, por favor asegurate de [clonar el repo](#clonar-repositorio) y [establecer la configuración general]( #establecer-configuracion-de-entorno-de-aplicacion)

### Clonar repositorio

``` bash
  $ git clone  git@github.com:sporter-management/product_api_service.git
        git clone output...
```

Ahora ingresa al directorio del proyecto, es decir, debes encontrarte aquí:

``` bash
    product_api_service < --- aqui procederemos con la instalación y configuración
    ├── .gitignore
    ├── LICENSE
    ├── .python-version
    ├── README.md
    ├── requirements.txt
    ├── TODO.md
    ├── nombre_del_entorno_virtual
    ├── dev_setup
    ├── .git
    └── product_api_service
```

### Establecer configuracion de entorno de aplicacion

Crea un archivo llamado `.env` y copia la siguiente configuración:

``` bash
# MYSQL Congiguration
    # Preferiblemente no cambiar
    MYSQL_DRIVERNAME=mysql+mysqlconnector

    # Las demás variables puedes cambiarlas a gusto

    # Configuración de conexión con mysql
    MYSQL_USERNAME=tu_nombre_de_usuario_mysql
    MYSQL_PASSWORD=tu_contraseña_de_usuario_mysql
    MYSQL_HOST=host_de_mysql
    MYSQL_PORT=3306
    MYSQL_DATABASE=sporter_product_database

    # Almacenamiento de imagenes
    HOST_FILES_DIR=/camino/a/donde/guardar/imagenes

    # Datos de admin del sitio
    APP_ADMIN_NAME=admin
    APP_ADMIN_PASS=password
    APP_ADMIN_EMAIL=admin@example.com

    # Configuracion para Docker

    # nombre del contenedor de la API
    API_CONTAINER_NAME=sporter_api
    # nombre del contenedor de la base de datos
    DB_CONTAINER_NAME=sporter_database
    # nombre del volumen para persistir tu base de datos
    API_DATABASE_VOLUME=sporter_database_volume

    # dónde montar el directorio de imagenes en el contenedor
    FILES_DIR=/images

    # Descomenta la siguiente línea para sobreescribir el host de la base de datos
    # Es decir, cambiar el host definido previamente por sporter_db
    # MYSQL_HOST=sporter_db

```

Asegurate de cambiar los valores según tu entorno.

### Instalación en tu sistema

#### Requerimientos

- Python 3.10 (preferiblemente) o mayor
- MySQL 8.4 o mayor

#### Entorno Virtual y dependencias de la API

Dentro del directorio del proyecto, crear un entorno virtual:

``` bash
    $ python3 -m venv <nombre_del_entorno_virtual>
```

Y activarlo:

``` bash
    # en Linux
    $ source nombre_del_entorno_virtual/bin/activate
    # en Windows
    $ nombre_del_entorno_virtual\\Scripts\\activate
```

Instalar las dependencias:

``` bash
    $ pip install -r requirements.txt
```

#### Levantar la Base de Datos

Asegurate de tener MySQL corriendo y de que la configuración es la correcta, ahora podrás crear la base de datos y sus schemas:

``` bash
    $ flask --app product_api_service db-cli crear-todo
```

Ahora puedes verificar que la base de datos haya sido creada, su nombre será el que se definió en `MYSQL_DATABASE`.

#### Levantar el servidor de la API

``` bash
    $ gunicorn --reload -w 3 -b 0.0.0.0:5000 "product_api_service:create_app()" --access-logfile -
```

### Despliegue con Docker

Ahora tambien puedes desplegar la API de Sporter con Docker Compose. Asegurate de tener tu archivo `.env` completo y correcto. Asegurate de cambiar el valor de `MYSQL_HOST` a `sporter_db`, de esta manera el contenedor de la API podrá hallar el servicio de MySQL dentro de la red Docker en que se hallan, dejamos una línea cometada para hacerlo más facil.


Aquí puedes ver el [archivo de configuración de compose](./docker-compose.yaml).
Para desplegar la aplicación:

``` bash
    $ docker compose up
```
