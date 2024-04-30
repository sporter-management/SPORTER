# Despliegue con DOCKER de SPORTER

## 1. Requisitos y disclaimer

> AVISO
>
> Las siguientes indicaciones suponen que te hallas en un sistema Linux
> Por lo tanto se recomienda usar uno o configurar WSL para poder usar Docker
> como en Linux nativo

Para desplegar este proyecto de manera correcta necesitarás:

- Docker Engine y Docker Compose instalados
- MySQL instalado
- El [repositorio de la api](https://github.com/sporter-management/product_api_service)  de sporter
- El [repositorio del frontend](https://github.com/sporter-management/web_frontend)  de sporter
- Leer atentamente este archivo y [la referencia de configuración del entorno](./env/reference.env)

Es preferible que los directorios de backend y frontend se hallen de manera adyacente a este:

``` bash
.
├── product_api_service
├── web_frontend
└── despliegue
```

De otra manera, presta atención a la última sección del [archivo de referencia del entorno](./env/reference.env)

## 2. Vistazo general de docker

### Crear un volumen para la base de datos

Los contenedores son efímeros, la información almacenada en ellos puede seguir existiendo si estos se paran pero se pierde una vez estos son removidos por suerte Docker cuenta con volúmenes que pueden montarse a los contenedores para así persistir datos más allá de la vida de un contenedor.

Necesitarás crear uno para la base de datos, puedes hacerlo de la siguiente manera:

``` bash
$ docker volume create sporter_db_volume 
```

Ese es el nombre que hemos establecido por defecto en el [archivo de configuracion de entorno](./env/reference.env), si necesitas usar otro, asegura de cambiar el valor de la variable `API_DATABASE_VOLUME`.

### Docker Compose

Docker compose permite definir la configuración de varios contenedores al mismo tiempo en un solo archivo, facilitando el despliegue de apliaciones multicontenedor así como su control.

Aquí puedes ver nuestro archivo [docker-compose](./docker-compose.yaml).

Para usar Compose debes correr el siguiente comando:

``` bash
$ docker compose up
```

¡Pero aún no estamos listos! Por favor sigue leyendo.

## 3. Configurar el entorno de despliegue

Para evitar escribir los parámetros de configuración de manera estática en `docker-compose.yaml`, se pueden utilizar archivos `.env` para definir las variables de entorno que Compose utilizará. 

Si el archivo `.env` esta en el mismo directorio donde ejecutas a Compose (y se llama de esa misma manera), no es necesario indicar su úbicación, lo mismo sucede con el archivo `docker-compose.yaml`.

Para poder desplegar el proyecto de manera correcta, por favor procede a leer  [la referencia de configuración del entorno](./env/reference.env) y reemplaza los valores de las variables de entorno según corresponda. Si no quieres editar el archivo que cuenta con las explicaciones [contamos con uno sin los comentarios](./env/no-comments.env).

Una vez lo hayas completado puedes dejarlo en el mismo directorio `env` con un nombre cualquiera, en ese caso, deberas utilizar la bandera `--env-file ./camino/al/.env`, en este caso:

``` bash
$ docker compose --env-file ./env/archivo.env up
```

O puedes cambiar el nombre del archivo a `.env` y copiarlo al mismo nivel donde se halla `docker-compose.yaml` y así evitar usar la bandera `--env-file`

El archivo `.env` se ha incluído en `.gitignore` para evitar que agregues tus datos de configuración al repositorio (en caso que nombre así al archivo).

## 4. Desplegar el proyecto

Ahora que has configurado el entorno de Compose puedes desplegar el proyecto, si `.env` y `docker-compose.yaml` se hayan en el mismo directorio (dentro de `despliegue`) puedes hacerlo con el comando que mencionamos previamente:

``` bash
$ docker compose up
```

Docker Compose creará las imágenes y luego levantará los servicios en orden, pero no creará las imagenes cada vez que despliegues el proyecto, para forzarlo a re-contruirlas deber usar:

``` bash
$ docker compose up --force-recreate --renew-anon-volumes --build
```

> AVISO
>
> Aún no se ha agregado la configuración necesaria para implementar Healthchecks ni Watch, como watch no está disponible, las imágenes necesitan ser re-construidar luego de cada cambio.
