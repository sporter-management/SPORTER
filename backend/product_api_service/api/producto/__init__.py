from flask import Blueprint

product_bp = Blueprint(
    "producto",
    __name__,
    url_prefix="/producto",
)

from product_api_service.api.producto.crear import altaProduct
product_bp.add_url_rule("/crear", altaProduct.__name__, altaProduct, methods=["POST"])

from product_api_service.api.producto.leer import read_by_product_id, read_by_query
product_bp.add_url_rule("/<id>", read_by_product_id.__name__,read_by_product_id, methods=["GET"])
product_bp.add_url_rule("/", read_by_query.__name__, read_by_query, methods=["GET"])

from product_api_service.api.producto.actualizar import update_existingProduct
product_bp.add_url_rule("/actualizar", update_existingProduct.__name__, update_existingProduct, methods=["POST"])

from product_api_service.api.producto.eliminar import eliminar_producto
product_bp.add_url_rule("/eliminar/<id_producto>", eliminar_producto.__name__, eliminar_producto, methods=["POST"])
