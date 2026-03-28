import os

HOST = os.getenv('DB_HOST', 'localhost')
USER = os.getenv('DB_USER', 'root')
PASSWORD = os.getenv('DB_PASSWORD', 'password_que_quieras_para_root')
DATABASE = os.getenv('DB_NAME', 'exampleDb')
PORT = os.getenv('DB_PORT', '3306')