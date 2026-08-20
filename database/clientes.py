from database.connection import conectar


def agregar_cliente(nombre, rut):
    conexion = conectar()

    if conexion is None:
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
        INSERT INTO clientes (nombre, rut)
        VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (nombre, rut)
        )

        conexion.commit()

        return cursor.lastrowid

    except Exception as e:
        print("Error al agregar cliente:", e)
        conexion.rollback()
        return None

    finally:
        if cursor:
            cursor.close()

        conexion.close()


def existe_rut(rut):
    conexion = conectar()

    if conexion is None:
        return False

    cursor = None

    try:
        cursor = conexion.cursor()

        sql = """
        SELECT id_cliente
        FROM clientes
        WHERE rut = %s
        """

        cursor.execute(
            sql,
            (rut,)
        )

        cliente = cursor.fetchone()

        return cliente is not None

    except Exception as e:
        print("Error al buscar RUT:", e)
        return False

    finally:
        if cursor:
            cursor.close()

        conexion.close()