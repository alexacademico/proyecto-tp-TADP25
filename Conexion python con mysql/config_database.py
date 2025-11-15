"""
Archivo de configuración para la base de datos MySQL
Manejo seguro de credenciales usando variables de entorno
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test_db'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': True
}

# Configuración alternativa para PyMySQL
PYMYSQL_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test_db'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4'
}

def get_database_config():
    """
    Retorna la configuración de la base de datos
    """
    return DATABASE_CONFIG

def get_pymysql_config():
    """
    Retorna la configuración para PyMySQL
    """
    return PYMYSQL_CONFIG


