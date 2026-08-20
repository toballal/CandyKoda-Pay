import flet as ft

from views.readNFC import read_view
from views.card_new import card_new_view
from views.card_result import card_result_view
from views.ruleta import roulette_view
from views.card_exist import card_exists_view

def main(page: ft.Page):
    page.title = "Candy Koda Pay"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme_seed="#9B59FF",
        font_family="Segoe UI",
        visual_density=ft.VisualDensity.COMFORTABLE,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.FADE_FORWARDS,
            linux=ft.PageTransitionTheme.FADE_FORWARDS,
            macos=ft.PageTransitionTheme.CUPERTINO,
            android=ft.PageTransitionTheme.FADE_UPWARDS,
            ios=ft.PageTransitionTheme.CUPERTINO,
        ),
    )
    page.bgcolor = "#09090F"
    page.window.full_screen  = True
    page.padding = 0
    page.spacing = 0


    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                read_view(page)
            )
        elif page.route == "/card_new":
            page.views.append(
                card_new_view(page)
            )
        elif page.route == "/card_result":
            page.views.append(
                card_result_view(page)
            )
        elif page.route == "/ruleta":
            page.views.append(
                roulette_view(page)
            )
        elif page.route == "/card_exists":
            page.views.append(
                card_exists_view(page)
            )
        else:
            page.route = "/"
            page.views.append(read_view(page))

        page.update()


    page.on_route_change = route_change

    page.route = "/"
    route_change(None)


ft.run(
    main,
    assets_dir="assets"
)
