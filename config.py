import os

class Config:
    # Clave secreta para JWT
    JWT_SECRET_KEY = 'yK7m2F!sD9lQzT3pA5vR&gB1wJ8eKfUx'

    # Configuración de la base de datos (usa PostgreSQL)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Ingeniero9!@mydevopsdb.cz6oaaici9tq.us-east-1.rds.amazonaws.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
