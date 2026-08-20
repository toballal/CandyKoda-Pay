from database.connection import conectar

import hashlib

def existe_tarjeta(uid):
    conexion = conectar()

    if conexion == None:
        print("No se pudo conectar a la base de datos")
        return False

    cursor = None

    try:
        cursor = conexion.cursor()
        sql = "SELECT id_tarjeta FROM tarjetas_nfc WHERE uid = %s"

        cursor.execute(
            sql,
            (uid,)
        )

        tarjeta = cursor.fetchone()

        return tarjeta is not None

    except Exception as e:
        print("Error al buscar tarjeta:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        conexion.close()

def agregar_tarjeta(id_cliente, uid, saldo, pin):
    conexion = conectar()

    if conexion == None:
        print("No se pudo conectar a la base de datos")
        return False

    cursor = None

    try:
        pin_hash = hashlib.sha256(
            pin.encode("utf-8")
        ).hexdigest()

        cursor = conexion.cursor()

        sql = "INSERT INTO tarjetas_nfc (id_cliente, uid, saldo, pin_hash) VALUES (%s, %s, %s, %s)"

        cursor.execute(
            sql,
            (id_cliente, uid, saldo, pin_hash)
        )

        conexion.commit()

        return True


    except Exception as e:
        print("No se pudo agregar la tarjeta:", e)

        conexion.rollback()

        return False
    finally:
        if cursor:
            cursor.close()

        conexion.close()

def obtener_datos_tarjeta(uid):
    conexion = conectar()

    if conexion is None:
        return None

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT
            t.id_tarjeta,
            t.uid,
            t.saldo,
            c.id_cliente,
            c.nombre,
            c.rut
        FROM tarjetas_nfc t
        INNER JOIN clientes c
            ON t.id_cliente = c.id_cliente
        WHERE t.uid = %s
        """

        cursor.execute(sql, (uid,))

        return cursor.fetchone()

    except Exception as e:
        print("Error al obtener datos:", e)
        return None

    finally:
        if cursor:
            cursor.close()

        conexion.close()

