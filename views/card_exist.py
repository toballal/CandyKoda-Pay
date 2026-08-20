import flet as ft

from database.tarjetas import obtener_datos_tarjeta
from components.theme import (
    TEXTO, TEXTO_2, MORADO, ROSA, marca, insignia, orbe, panel, fondo,
    boton_primario,
)


def card_exists_view(page: ft.Page):

    uid = page.data["uid"]

    datos = obtener_datos_tarjeta(uid)

    if datos is None:
        return ft.View(
            route="/card_exists",
            controls=[
                ft.Text("No se pudieron obtener los datos")
            ],
        )

    contenido = panel(
        ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                marca(32),
                insignia("TARJETA RECONOCIDA", ft.Icons.VERIFIED_ROUNDED),
                orbe(ft.Icons.ACCOUNT_BALANCE_WALLET_ROUNDED, size=82),

                ft.Text(
                    "Mi cuenta",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                ),

                # DATOS DEL CLIENTE
                ft.Container(
                    width=450,
                    padding=20,
                    bgcolor="#1B1B29",
                    border_radius=16,
                    border=ft.Border.all(1, "#34344A"),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PERSON_ROUNDED,
                                        color=ROSA,
                                    ),
                                    ft.Text(
                                        "Datos del cliente",
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXTO,
                                    ),
                                ],
                            ),

                            ft.Text(
                                f"Nombre: {datos['nombre']}",
                                size=17,
                                color=TEXTO,
                            ),

                            ft.Text(
                                f"RUT: {datos['rut']}",
                                size=17,
                                color=TEXTO,
                            ),

                            ft.Text(
                                f"UID: {datos['uid']}",
                                size=17,
                                color=TEXTO_2,
                            ),
                        ],
                    ),
                ),

                # SALDO
                ft.Container(
                    width=450,
                    padding=18,
                    gradient=ft.LinearGradient(colors=["#281A39", "#1B1B29"]),
                    border_radius=16,
                    border=ft.Border.all(1, "#51356F"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Text(
                                "Saldo disponible",
                                size=16,
                                color=TEXTO_2,
                            ),

                            ft.Text(
                                f"${datos['saldo']:,.0f}",
                                size=38,
                                weight=ft.FontWeight.BOLD,
                                color=TEXTO,
                            ),
                        ],
                    ),
                ),

                boton_primario("Finalizar", ft.Icons.CHECK_ROUNDED, lambda e: page.navigate("/"), 450),
            ],
        ), width=520, padding=24,
    )
    # El panel puede ser más alto que la ventana (por ejemplo 720p). El scroll
    # conserva el botón accesible y el wrapper mantiene el centrado horizontal.
    pantalla = fondo(
        ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[contenido],
        ),
        padding=20,
    )

    return ft.View(
        route="/card_exists",
        bgcolor="#09090F",
        padding=0,
        spacing=0,
        controls=[
            pantalla
        ],
    )
