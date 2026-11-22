import flet as ft
import component


def build_detail_view(data):
        region_name = data[0]
        wild = data[1]
        # print(f"/wild/{region_name}/{wild['id']}")
        return ft.View(
            route=f"/wild/{region_name}/{wild['id']}",
            appbar=ft.AppBar(
                title=ft.Text(wild['name'])
            ),
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,

                        controls=[
                            component.build_hero(wild, 400, 220),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls= [
                                    ft.Text(
                                        wild['name'],
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color="#007FA9",
                                    ),
                                    ft.Text(
                                        f"#{wild['id']:04}",
                                        size=18,
                                    ),
                                ]
                            ),                            

                            ft.Container(
                                bgcolor="#DDF8F2",
                                padding=12,
                                border_radius=15,
                                content=ft.Text(
                                    f"Type: {wild['type']}",
                                    size=18,
                                ),
                            ),

                            ft.Container(
                                padding=15,
                                content=ft.Text(
                                    wild["description"],
                                    text_align=ft.TextAlign.CENTER,
                                    size=16,
                                ),
                            ),

                            ft.Button(
                                "Back to collection",
                                on_click= component.get_nav(component.page, "go_back",),
                            )
                        ],
                    ),
                ),
            ],
        )