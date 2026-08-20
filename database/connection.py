import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="candy_koda"
        )

        return conexion

    except Error as e:
        print("Error al conectar con MySQL:", e)
        return None