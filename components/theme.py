import flet as ft

FONDO = "#09090F"
SUPERFICIE = "#11111B"
CARD = "#161622"
CARD_ELEVADA = "#1B1B29"
BORDE = "#2A2A3A"
MORADO = "#9B59FF"
ROSA = "#FF4FA3"
VERDE = "#57D68D"
AMARILLO = "#FFC857"
ROJO = "#FF647C"
TEXTO = "#F7F7FB"
TEXTO_2 = "#A7A7B8"


def marca(size=32):
    return ft.Row(
        tight=True,
        spacing=4,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text("Candy", size=size, weight=ft.FontWeight.BOLD, color=MORADO),
            ft.Text("Koda", size=size, weight=ft.FontWeight.BOLD, color=ROSA),
            ft.Text("Pay", size=size, weight=ft.FontWeight.BOLD, color=TEXTO),
        ],
    )


def insignia(texto, icono=ft.Icons.CONTACTLESS_ROUNDED, color=MORADO):
    return ft.Container(
        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
        bgcolor=ft.Colors.with_opacity(0.12, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.35, color)),
        border_radius=20,
        content=ft.Row(
            tight=True,
            spacing=7,
            controls=[
                ft.Icon(icono, size=15, color=color),
                ft.Text(texto, size=11, color=color, weight=ft.FontWeight.BOLD),
            ],
        ),
    )


def orbe(icono, color=ROSA, size=128):
    return ft.Container(
        width=size,
        height=size,
        border_radius=size / 2,
        gradient=ft.RadialGradient(colors=["#2A1A3A", CARD_ELEVADA]),
        border=ft.Border.all(2, ft.Colors.with_opacity(0.75, MORADO)),
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(blur_radius=34, color="#4D9B59FF"),
        content=ft.Icon(icono, size=size * 0.48, color=color),
    )


def panel(content, width=520, padding=32):
    return ft.Container(
        width=width,
        padding=padding,
        bgcolor=ft.Colors.with_opacity(0.96, CARD),
        border=ft.Border.all(1, BORDE),
        border_radius=24,
        shadow=ft.BoxShadow(blur_radius=35, color="#55000000", offset=ft.Offset(0, 12)),
        content=content,
    )


def fondo(content, padding=30):
    return ft.Container(
        expand=True,
        padding=padding,
        gradient=ft.RadialGradient(
            center=ft.Alignment(-0.75, -0.85),
            radius=1.35,
            colors=["#211332", FONDO, "#08080D"],
            stops=[0, 0.46, 1],
        ),
        alignment=ft.Alignment.CENTER,
        content=content,
    )


def boton_primario(texto, icono, on_click, width=456):
    return ft.FilledButton(
        texto,
        icon=icono,
        width=width,
        height=54,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=MORADO,
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )


def boton_secundario(texto, icono, on_click, width=456):
    return ft.OutlinedButton(
        texto,
        icon=icono,
        width=width,
        height=52,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=TEXTO,
            side=ft.BorderSide(1, "#4A3A61"),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )


def campo(**kwargs):
    defaults = dict(
        height=58,
        border_radius=12,
        bgcolor=CARD_ELEVADA,
        border_color="#34344A",
        focused_border_color=MORADO,
        color=TEXTO,
        cursor_color=ROSA,
    )
    defaults.update(kwargs)
    return ft.TextField(**defaults)
