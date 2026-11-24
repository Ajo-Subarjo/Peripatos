import flet as ft
import component


def build_detail_view(data):
        region_name = data[0]
        wild = data[1]
        # print(f"/wild/{region_name}/{wild['id']}")
        return ft.View(
            appbar=ft.AppBar(title=ft.Text(wild['name']),bgcolor="#356859"),
            padding=0,
            bgcolor="#e8eeed",
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=ft.Hero(
                        tag=component.card_tag(region_name,wild['id']),
                        transition_on_user_gestures=True,
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.START,                                    
                            controls=[
                                component.build_image(region_name, wild, 450, 220),
                                ft.Container(
                                    padding=10,
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.START,
                                        controls= [
                                            ft.Text(
                                                wild['name'],
                                                size=28,
                                                weight=ft.FontWeight.BOLD,
                                                color="#483B46",
                                            ),
                                            ft.Text(
                                                f"#{wild['id']:04}",
                                                size=18,
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
                                                on_click= component.get_nav("go_back")
                                            ),
                                        ]
                                    )
                                )
                            ],
                        )
                    )
                )
            ]
        )
                                    

        