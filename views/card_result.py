import flet as ft

from database.clientes import agregar_cliente
from database.tarjetas import agregar_tarjeta
from components.theme import (
    TEXTO, TEXTO_2, MORADO, ROSA, VERDE, ROJO, marca, insignia, orbe,
    panel, fondo, boton_primario, boton_secundario,
)

def card_result_view(page: ft.Page):

    # Obtener resultado guardado anteriormente
    resultado = {}

    if isinstance(page.data, dict):
        resultado = page.data

    exito = resultado.get("exito", False)
    mensaje = resultado.get(
        "mensaje",
        "No se pudo completar la operación"
    )

    # -------------------------
    # CONFIGURACIÓN SEGÚN RESULTADO
    # -------------------------

    if exito:
        color = VERDE
        color_icono = VERDE
        icono = ft.Icons.CHECK_CIRCLE_ROUNDED
        titulo = "¡Tarjeta activada!"
        descripcion = "Tu tarjeta Candy Koda fue activada correctamente."

        saldo_inicial = page.data["premio"]
        saldo_inicial = saldo_inicial.replace("$", "")

        uid = page.data["uid"]
        nombre = page.data["nombre"]
        rut = page.data["rut"]
        pin = page.data["pin"]
        saldo = float(page.data["premio"])

        # La vista puede reconstruirse por navegación o resize. Registrar una
        # sola vez evita clientes/tarjetas duplicados por un efecto visual.
        if not page.data.get("registro_completado", False):
            id_cliente = agregar_cliente(nombre, rut)
            agregar_tarjeta(id_cliente, uid, saldo, pin)
            page.data["registro_completado"] = True
    else:
        color = ROJO
        color_icono = ROJO
        icono = ft.Icons.ERROR_OUTLINE_ROUNDED
        titulo = "No pudimos activar la tarjeta"
        descripcion = mensaje

    # -------------------------
    # PANTALLA
    # -------------------------

    contenido = panel(
        ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=17,
            controls=[
                marca(32),
                insignia("OPERACIÓN COMPLETADA" if exito else "REQUIERE ATENCIÓN", icono, color),
                orbe(icono, color_icono, 122),

                # TÍTULO
                ft.Text(
                    titulo,
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                    text_align=ft.TextAlign.CENTER,
                ),

                # DESCRIPCIÓN
                ft.Text(
                    descripcion,
                    size=17,
                    color=TEXTO_2,
                    text_align=ft.TextAlign.CENTER,
                ),

                # SALDO INICIAL
                ft.Container(
                    visible=exito,
                    width=400,
                    padding=20,
                    gradient=ft.LinearGradient(colors=["#281A39", "#1B1B29"]),
                    border_radius=15,
                    border=ft.Border.all(
                        1,
                        "#51356F",
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Text(
                                "Saldo inicial",
                                size=15,
                                color=TEXTO_2,
                            ),
                            ft.Text(
                                f"${saldo_inicial}",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=TEXTO,
                            ),
                        ],
                    ),
                ),

                ft.Container(height=10),

                # FINALIZAR
                ft.Container(
                    visible=exito,
                    content=boton_primario("Finalizar", ft.Icons.CHECK_ROUNDED, lambda e: page.navigate("/"), 400),
                ),

                # REINTENTAR
                ft.Container(
                    visible=not exito,
                    content=boton_primario("Reintentar", ft.Icons.REFRESH_ROUNDED, lambda e: page.navigate("/card_new"), 400),
                ),

                # CANCELAR
                ft.Container(
                    visible=not exito,
                    content=boton_secundario("Cancelar", ft.Icons.CLOSE_ROUNDED, lambda e: page.navigate("/"), 400),
                ),
            ],
        ), width=500, padding=34,
    )
    pantalla_resultado = fondo(contenido)
    return ft.View(
        route="/card_result",
        bgcolor="#09090F",
        padding=0,
        spacing=0,
        controls=[
            pantalla_resultado
        ],
    )
