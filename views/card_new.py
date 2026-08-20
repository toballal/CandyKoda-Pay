import flet as ft

from database.clientes import existe_rut
from components.theme import (
    TEXTO, TEXTO_2, ROSA, marca, insignia, orbe, panel, fondo,
    boton_primario, boton_secundario, campo,
)


def card_new_view(page: ft.Page):

    # -------------------------
    # CAMPOS
    # -------------------------

    nombre = campo(
        label="Nombre completo",
        hint_text="Ej: Cristóbal Osorio",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        max_length=100,
        width=500,
    )

    rut = campo(
        label="RUT",
        hint_text="Ej: 12345678-9",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        width=500,
    )

    pin = campo(
        label="PIN",
        hint_text="Ingresa un PIN de 4 dígitos",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        width=500,
        password=True,
        can_reveal_password=True,
        max_length=4,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    error = ft.Text(
        "",
        size=14,
        color=ROSA,
        visible=False,
    )

    # -------------------------
    # CONTINUAR
    # -------------------------

    def continuar(e):

        nombre_texto = nombre.value.strip()
        rut_texto = rut.value.strip()
        pin_texto = pin.value.strip()

        # NOMBRE
        if nombre_texto == "":
            error.value = "Ingresa tu nombre"
            error.visible = True
            page.update()
            return

        if len(nombre_texto) < 3:
            error.value = "El nombre es demasiado corto"
            error.visible = True
            page.update()
            return

        if len(nombre_texto) > 100:
            error.value = "El nombre no puede superar los 100 caracteres"
            error.visible = True
            page.update()
            return

        if not nombre_texto.replace(" ", "").isalpha():
            error.value = "El nombre solo puede contener letras"
            error.visible = True
            page.update()
            return


        # RUT
        rut_texto = rut.value.strip().upper()

        if rut_texto == "":
            error.value = "Ingresa tu RUT"
            error.visible = True
            page.update()
            return

        if "-" not in rut_texto:
            error.value = "El RUT debe contener un guion"
            error.visible = True
            page.update()
            return

        partes = rut_texto.split("-")

        if len(partes) != 2:
            error.value = "RUT inválido"
            error.visible = True
            page.update()
            return

        numero, dv = partes

        if not numero.isdigit():
            error.value = "El RUT antes del guion solo puede contener números"
            error.visible = True
            page.update()
            return

        if not (dv.isdigit() or dv == "K"):
            error.value = "Dígito verificador inválido"
            error.visible = True
            page.update()
            return

        if existe_rut(rut_texto):
            error.value = "Este RUT ya está registrado"
            error.visible = True
            page.update()
            return

        # PIN
        if pin_texto == "":
            error.value = "Ingresa un PIN"
            error.visible = True
            page.update()
            return

        if len(pin_texto) != 4:
            error.value = "El PIN debe tener 4 dígitos"
            error.visible = True
            page.update()
            return

        if not pin_texto.isdigit():
            error.value = "El PIN solo puede contener números"
            error.visible = True
            page.update()
            return

        error.visible = False
        page.update()

        # Obtener UID leído anteriormente
        uid = None

        if isinstance(page.data, dict):
            uid = page.data.get("uid")

        # Guardar todos los datos
        page.data = {
            "uid": uid,
            "nombre": nombre.value.strip(),
            "rut": rut.value.strip(),
            "pin": pin.value,
            "premio": None,

            "exito": True,
            "mensaje": "Tarjeta registrada correctamente"
        }

        print(page.data)

        # Ir a pantalla de resultado
        page.navigate("/ruleta")

    # -------------------------
    # PANTALLA
    # -------------------------

    contenido = panel(
        ft.Column(
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                marca(30),
                insignia("NUEVA TARJETA", ft.Icons.ADD_CARD_ROUNDED),
                orbe(ft.Icons.ADD_CARD_ROUNDED, size=92),

                # TÍTULO
                ft.Text(
                    "Activa tu tarjeta",
                    size=27,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                ),

                ft.Text(
                    "Ingresa tus datos para vincular tu tarjeta Candy Koda",
                    size=16,
                    color=TEXTO_2,
                    text_align=ft.TextAlign.CENTER,
                ),

                # CAMPOS
                nombre,

                rut,

                pin,

                # ERROR
                error,

                # CONTINUAR
                boton_primario("Continuar", ft.Icons.ARROW_FORWARD_ROUNDED, continuar, 500),

                # CANCELAR
                boton_secundario("Cancelar", ft.Icons.CLOSE_ROUNDED, lambda e: page.navigate("/"), 500),
            ],
        ), width=570, padding=26,
    )
    pantalla_activar = fondo(
        ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[contenido],
        ), padding=24,
    )

    # -------------------------
    # VIEW
    # -------------------------

    return ft.View(
        route="/card_new",
        bgcolor="#09090F",
        padding=0,
        spacing=0,
        controls=[
            pantalla_activar
        ],
    )
