import asyncio
import flet as ft

from hardware.arduino import leer_tarjeta
from database.tarjetas import existe_tarjeta
from components.theme import (
    TEXTO, TEXTO_2, MORADO, marca, insignia, orbe, panel, fondo
)


def read_view(page: ft.Page):

    async def esperar_tarjeta():
        while page.route == "/":

            uid = leer_tarjeta()

            if uid is not None:
                print("Tarjeta detectada:", uid)

                page.data = {
                    "uid": uid
                }

                if existe_tarjeta(uid):
                    print("Tarjeta ya registrada")
                    await page.push_route("/card_exists")
                else:
                    print("Tarjeta nueva")
                    await page.push_route("/card_new")

                break

            await asyncio.sleep(0.1)

    contenido = panel(
        ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                marca(34),
                insignia("PAGO SIN CONTACTO"),
                ft.Container(height=4),
                ft.Text(
                    "Acerca tu tarjeta",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                ),
                ft.Text(
                    "Acerca tu tarjeta Candy Koda al lector NFC",
                    size=15,
                    color=TEXTO_2,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=6),
                ft.Stack(
                    width=164, height=164,
                    alignment=ft.Alignment.CENTER,
                    controls=[
                        ft.ProgressRing(width=164, height=164, stroke_width=3, color=MORADO),
                        orbe(ft.Icons.CONTACTLESS_ROUNDED, size=138),
                    ],
                ),
                ft.Container(height=4),
                ft.Text(
                    "Esperando tarjeta...",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=MORADO,
                ),
                ft.Text("Mantén la tarjeta cerca del lector", size=12, color=TEXTO_2),
            ],
        ), width=520, padding=38,
    )
    pantalla_espera = fondo(contenido)

    page.run_task(esperar_tarjeta)

    return ft.View(
        route="/",
        bgcolor="#09090F",
        padding=0,
        spacing=0,
        controls=[
            pantalla_espera
        ],
    )
