import flet as ft

from view.login_view import vista_login


def main(page: ft.Page):

    page.title = "OpenMarket"

    page.window_width = 1400

    page.window_height = 800

    page.padding = 0

    page.theme_mode = ft.ThemeMode.LIGHT

    page.bgcolor = "#F5F7FA"

    page.horizontal_alignment = "center"

    page.vertical_alignment = "center"

    page.add(

        vista_login(page)
    )


ft.app(target=main)