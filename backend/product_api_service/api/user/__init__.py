from flask import Blueprint

user_bp=Blueprint("user", __name__, url_prefix="/user")

from product_api_service.api.user.crear import register_user
user_bp.add_url_rule("/register", register_user.__name__, register_user, methods=["POST"])

from product_api_service.api.user.actualizar import update_user
user_bp.add_url_rule("/actualizar", update_user.__name__, update_user, methods=["POST"])

from product_api_service.api.user.leer import read_by_product_id, read_by_query
user_bp.add_url_rule("/", read_by_query.__name__, read_by_query, methods=["GET"])
user_bp.add_url_rule("/<id>", read_by_product_id.__name__, read_by_product_id, methods=["GET"])

from product_api_service.api.user.eliminar import eliminar_usuario
user_bp.add_url_rule("/eliminar/<id_usuario>", eliminar_usuario.__name__, eliminar_usuario, methods=["POST"])

from product_api_service.api.user.login import login
user_bp.add_url_rule("/login", login.__name__, login, methods=["POST"])