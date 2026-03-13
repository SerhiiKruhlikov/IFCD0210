import mysql.connector
import config 

def get_connection():
    conexion = mysql.connector.connect(
        host = config.HOST,
        user = config.USER,
        port = config.PORT,
        password = config.PASSWORD,
        database = config.DATABASE
    )
    return conexion

def ejecutar_sql(sql_command,*args):
    cnx = get_connection()
    cursor = cnx.cursor()
    
    cursor.execute(sql_command,*args)

    resultado = cursor.fetchall()

    cursor.close()
    cnx.close()

    return resultado


def prueba():

    #resultado = ejecutar_sql('call contar_gama(%s)',('Frutales',))
    resultado = ejecutar_sql(
        'select * from producto where codigo_producto=%s',(11679,))

    for fila in resultado:
        print(fila)


prueba()