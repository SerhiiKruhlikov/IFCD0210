import sqlite3

cnx = sqlite3.connect("facturas.sqlite")
with open("respaldo.sql","w") as f:
    for linea in cnx.iterdump():
        f.write(f'{linea}\n')

cnx.close()