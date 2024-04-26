from flask import Blueprint, jsonify


service_api = Blueprint("api", __name__, url_prefix="/api")

from product_api_service.api.producto import product_bp
service_api.register_blueprint(product_bp)

from product_api_service.api.etiqueta import etiqueta_bp
service_api.register_blueprint(etiqueta_bp)

from product_api_service.api.user import user_bp
service_api.register_blueprint(user_bp)