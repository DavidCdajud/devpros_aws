from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import datetime
from model import db, Blacklist
from config import Config

# Inicializa la aplicación Flask
application = Flask(__name__)  # Cambia 'app' a 'application'
application.config.from_object(Config)

# Inicializa las extensiones
db.init_app(application)
jwt = JWTManager(application)

# Crear las tablas de la base de datos si no existen
with application.app_context():
    db.create_all()

# Ruta para autenticarse y obtener un token JWT
@application.route('/login', methods=['POST'])
def login():
    # En un caso real, verificarías el usuario y contraseña, aquí lo simplificamos
    access_token = create_access_token(identity='test_user')
    return jsonify(access_token=access_token), 200

# Endpoint para agregar un email a la lista negra (POST)
@application.route('/blacklists', methods=['POST'])
@jwt_required()
def add_email_to_blacklist():
    data = request.get_json()

    # Validar los datos recibidos
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    blocked_reason = data.get('blocked_reason', '')

    # Verificar si el email ya existe en la lista negra
    if Blacklist.query.filter_by(email=email).first():
        return jsonify({'message': 'Email is already in the blacklist'}), 400

    # Obtener la IP del solicitante
    ip_address = request.remote_addr

    # Crear un nuevo registro en la lista negra
    new_blacklist_entry = Blacklist(
        email=email,
        app_uuid=app_uuid,
        blocked_reason=blocked_reason,
        ip_address=ip_address
    )
    db.session.add(new_blacklist_entry)
    db.session.commit()

    return jsonify({'message': 'Email added to blacklist'}), 201

# Endpoint para consultar si un email está en la lista negra (GET)
@application.route('/blacklists/<string:email>', methods=['GET'])
@jwt_required()
def check_email_in_blacklist(email):

    # Buscar si el email está en la lista negra
    blacklist_entry = Blacklist.query.filter_by(email=email).first()

    if blacklist_entry:
        return jsonify({
            'email': email,
            'in_blacklist': True,
            'blocked_reason': blacklist_entry.blocked_reason
        }), 200
    else:
        return jsonify({'email': email, 'in_blacklist': False}), 404
    

@application.route('/', methods=['GET'])
def health_check():
    return "pong", 200



if __name__ == '__main__':
    application.run(port=5000, host='0.0.0.0')
