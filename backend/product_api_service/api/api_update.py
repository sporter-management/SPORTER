from typing import Dict
from flask import Blueprint, jsonify, request
from sqlalchemy import select, update, delete, or_
from sqlalchemy.exc import IntegrityError
from product_api_service.database.session import create_local_session
from product_api_service import schemas, models
from pydantic import ValidationError
import os 
from werkzeug.utils import secure_filename
import uuid 

updateProduct_bp = Blueprint(
    "updateProduct",
    __name__,
    url_prefix="/producto",
)

@updateProduct_bp.post("/actualizar")
def update_existingProduct():

    # Verificar si el nombre de la imagen ha sido enviado
    if 'filename' in UpdateFiles:
        imagen = UpdateFiles["filename"]
        if not imagen.filename:  # Verificar si el nombre del archivo está vacío
            return {"msj": "Nombre de archivo de imagen inválido"}, 400
        
    # Obtener los datos de la solicitud incluyendo los archivos
    UpdateRequest: Dict = request.form.to_dict()
    UpdateFiles: Dict = request.files

    # Validar la solicitud incluyendo los archivos
    try:
        # Combinar datos de formulario y archivos en un solo diccionario
        UpdateData = {**UpdateRequest, **UpdateFiles}

        # Validar utilizando el esquema de Producto
        RequestValidada = schemas.Producto(**UpdateData).dict()

    except ValidationError as ve:
        errors_list = []
        for error in ve.errors():
            error_object = {
                "field": error["loc"][0],
                "invalid_input": error["input"],
                "error_info": error["msg"],
            }
            errors_list.append(error_object)

        return {"msj": "Informacion de ejemplo invalida", "errors": errors_list}, 400

    try:
        with create_local_session() as db_session:
            # Obtener la información del ejemplo antes de actualizar
            old_example = (
                db_session.query(models.Ejemplo)
                .filter(models.Ejemplo.id == RequestValidada["id"])
                .first()
            )

            # Con este se actualiza
            update_data = {
                "nombre": RequestValidada["nombre"],
                "descripcion": RequestValidada["descripcion"],
                "precio": RequestValidada["precio"],
                "cantidad": RequestValidada["cantidad"],
            }

            # Verificar si hay una nueva imagen
            if "filename" in UpdateRequest:
                imagen = UpdateFiles["filename"]
                # Generar un nombre único para la imagen
                img_rand_name = str(uuid.uuid4()) + secure_filename(imagen.filename)
                img_path = os.path.join(os.getenv('FILES_DIR'), img_rand_name)
                imagen.save(img_path)

                # Eliminar la imagen anterior si existe
                if old_example and old_example.img_rand_name:
                    old_image_path = os.path.join(os.getenv('FILES_DIR'), old_example.img_rand_name)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                update_data["img_orig_name"] = imagen.filename
                update_data["img_rand_name"] = img_rand_name

            update_example_query: update = (
                update(models.Ejemplo)
                .where(models.Ejemplo.id == RequestValidada["id"])
                .values(**update_data)
            )
            db_session.execute(update_example_query)
            db_session.commit()

    except IntegrityError as ie:
        campo_repetido = ie.orig.args[1].split(".")[-1].strip("'")
        return {"msj": f"El ejemplo que intento con {campo_repetido} crear ya existe "}, 400
    except Exception as e:
        db_session.rollback()
        return {"msj": "Error interno del servidor"}, 500

    return {"msj": f"Ejemplo {RequestValidada['nombre']} actualizado exitosamente"}, 200
