import mysql.connector

conexion = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    port = '3306',
    password = 'password_que_quieras_para_root',
    database = 'jardineria'
)

cursor = conexion.cursor()
cursor.execute('call contar_gama(%s)',('Frutales',))

resultado = cursor.fetchall()

cursor.close()
conexion.close()

for fila in resultado:
    print(fila)

