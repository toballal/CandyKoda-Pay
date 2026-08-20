import math
import random
import asyncio

import flet as ft
import flet.canvas as cv
from components.theme import FONDO, CARD, TEXTO, TEXTO_2, MORADO, ROSA, AMARILLO, marca, insignia


def roulette_view(page: ft.Page):

    premios = [
        "500",
        "800",
        "900",
        "1000",
        "1100",
        "1200",
    ]

    colores = [
        "#9B59FF",
        "#FF4FA3",
        "#FFC107",
        "#7A3FC7",
        "#E63B8B",
        "#D39D00",
    ]

    # Un diámetro algo menor deja espacio para títulos y acciones incluso en
    # resoluciones de kiosco bajas, sin provocar desbordamiento horizontal.
    size = 350
    centro = size / 2
    radio = 158

    shapes = []

    cantidad = len(premios)
    angulo_sector = 2 * math.pi / cantidad

    # -------------------------
    # CREAR RULETA
    # -------------------------

    for i, premio in enumerate(premios):

        inicio = -math.pi / 2 + i * angulo_sector

        shapes.append(
            cv.Arc(
                x=centro - radio,
                y=centro - radio,
                width=radio * 2,
                height=radio * 2,
                start_angle=inicio,
                sweep_angle=angulo_sector,
                use_center=True,
                paint=ft.Paint(
                    color=colores[i],
                    style=ft.PaintingStyle.FILL,
                ),
            )
        )

        angulo_texto = inicio + angulo_sector / 2

        x = centro + math.cos(angulo_texto) * 100
        y = centro + math.sin(angulo_texto) * 100

        shapes.append(
            cv.Text(
                x=x,
                y=y,
                value=f"${premio}",
                alignment=ft.Alignment.CENTER,
                style=ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                ),
            )
        )

    # Centro de la ruleta
    shapes.append(
        cv.Circle(
            x=centro,
            y=centro,
            radius=39,
            paint=ft.Paint(
                color="#121212",
                style=ft.PaintingStyle.FILL,
            ),
        )
    )

    canvas_ruleta = cv.Canvas(
        width=size,
        height=size,
        shapes=shapes,
    )

    # -------------------------
    # RULETA
    # -------------------------

    ruleta = ft.Container(
        width=size,
        height=size,
        alignment=ft.Alignment.CENTER,
        content=canvas_ruleta,
        rotate=ft.Rotate(
            angle=0,
            alignment=ft.Alignment.CENTER,
        ),
        animate_rotation=ft.Animation(
            duration=4000,
            curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        ),
    )

    resultado = ft.Text(
        "",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ROSA,
        text_align=ft.TextAlign.CENTER,
    )

    angulo_actual = 0

    def continuar(e):
        page.navigate("/card_result")

    # -------------------------
    # GIRAR
    # -------------------------

    async def girar(e):
        nonlocal angulo_actual

        boton_girar.disabled = True
        resultado.value = ""

        page.update()

        # Elegir premio
        premio_index = random.randint(
            0,
            len(premios) - 1
        )

        premio = premios[premio_index]

        # Centro del sector ganador
        centro_sector = (
            premio_index * angulo_sector
            + angulo_sector / 2
        )

        # Posición donde debe terminar
        angulo_objetivo = (
            -centro_sector
        ) % (2 * math.pi)

        posicion_actual = (
            angulo_actual
            % (2 * math.pi)
        )

        diferencia = (
            angulo_objetivo
            - posicion_actual
        ) % (2 * math.pi)

        # 5 vueltas completas
        giro = (
            5 * 2 * math.pi
            + diferencia
        )

        angulo_actual += giro

        # Girar ruleta
        ruleta.rotate.angle = angulo_actual

        page.update()

        # Esperar que termine de girar
        await asyncio.sleep(4)

        # Mostrar premio
        resultado.value = f"¡Ganaste: ${premio}!"

        # Guardar premio
        if isinstance(page.data, dict):
            page.data["premio"] = premio
        else:
            page.data = {
                "premio": premio
            }

        # CAMBIAR BOTÓN
        boton_girar.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_ROUNDED,
                    size=20,
                ),
                ft.Text(
                    "Continuar",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        )

        boton_girar.on_click = continuar
        boton_girar.disabled = False

        page.update()

        page.update()

    # -------------------------
    # BOTÓN
    # -------------------------

    boton_girar = ft.FilledButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(
                    ft.Icons.CASINO_ROUNDED,
                    size=20,
                ),
                ft.Text(
                    "Girar ruleta",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
        ),
        width=250,
        height=55,
        on_click=girar,
        style=ft.ButtonStyle(
            bgcolor=MORADO,
            color="#FFFFFF",
        ),
    )

    boton_volver = ft.OutlinedButton(
        "Volver",
        icon=ft.Icons.ARROW_BACK_ROUNDED,
        width=250,
        height=50,
        on_click=lambda e: page.navigate("/card_new"),
        style=ft.ButtonStyle(
            color="#FFFFFF",
            side=ft.BorderSide(
                1,
                MORADO,
            ),
        ),
    )

    # -------------------------
    # PANTALLA
    # -------------------------

    contenido_ruleta = ft.Container(
        width=520,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                marca(32),
                insignia("PREMIO DE BIENVENIDA", ft.Icons.AUTO_AWESOME_ROUNDED, AMARILLO),
                ft.Text(
                    "Ruleta de premios",
                    size=27,
                    weight=ft.FontWeight.BOLD,
                    color=TEXTO,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Gira la ruleta y descubre tu premio",
                    size=16,
                    color=TEXTO_2,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, size=38, color=AMARILLO),
                # La fila fuerza el centrado del canvas; algunos backends no
                # aplican CrossAxisAlignment al Canvas de forma consistente.
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[ruleta],
                ),
                resultado,
                boton_girar,
                boton_volver,
            ],
        ),
    )

    pantalla_ruleta = ft.Container(
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.Alignment(-0.75, -0.85), radius=1.35,
            colors=["#211332", FONDO, "#08080D"], stops=[0, 0.46, 1],
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=24),
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[contenido_ruleta],
        ),
    )

    # -------------------------
    # VIEW
    # -------------------------

    return ft.View(
        route="/ruleta",
        bgcolor=FONDO,
        padding=0,
        spacing=0,
        controls=[
            pantalla_ruleta
        ],
    )
