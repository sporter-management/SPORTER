from flask import Blueprint

from flask import Blueprint

etiqueta_bp=Blueprint("etiqueta", __name__, url_prefix="/etiqueta")

#@read_tag_bp.get("/<identificacion>")
#@read_tag_bp.get("/")

from product_api_service.api.etiqueta.leer import read_all, read_by_product_id
etiqueta_bp.add_url_rule("/leer/<identificacion>", read_all.__name__, read_all, methods=["GET"])
etiqueta_bp.add_url_rule("/leer/", read_by_product_id.__name__,read_by_product_id, methods=["GET"])