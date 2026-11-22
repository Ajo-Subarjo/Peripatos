import flet as ft
import component
from DB import get_grouped, get_regions

region_visible = []
regions_sections = []

def build_wildex_view():

    component.page.views.clear()
    
    grouped = get_grouped()

    filter_box = ft.Container(
        visible=False,
        padding=8,

        border_radius=8,
        bgcolor="#Ffffff",

        content=ft.Column(
            tight=True,
            height=min(len(grouped) * 50, 150),
            margin=ft.Margin(0,0,0,20),
            # scroll=ft.ScrollMode.AUTO,
            controls=[
                build_region_list_filter_button(),
            ]
        )
    )

    def toggle_filter():
        filter_box.visible = not filter_box.visible
        # print(filter_box.visible)

        component.page.update()

    regions_sections.clear()

    
    for region_name, wilds in grouped.items():
        
        cards = []


        for wild in wilds:
            cards.append(build_card(region_name, wild)) 


        regions_sections.append(
            ft.Column(
                data=region_name,
                controls=[
                    ft.Text(
                        region_name.replace("_", " ").title(),
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.GridView(
                        expand=True,
                        runs_count=2,
                        max_extent=180,
                        child_aspect_ratio=0.85,
                        spacing=8,
                        run_spacing=8,
                        controls= cards,
                    ),
                ],
                spacing=10
            )
        )

        
    return ft.View(
        route="/",
        appbar=ft.AppBar(
            title=ft.Text("WILDEX"),
        ),
        controls=[
            ft.SafeArea(
                expand=True,
                content=ft.Stack(
                    expand=True,
                    controls= [
                        ft.ListView(
                            expand=True,
                            spacing=4,
                            controls=regions_sections
                        ),
                        ft.Container(
                            width=150,
                            right=20,
                            bottom=20,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=-20,
                                controls= [
                                    filter_box,
                                    ft.FloatingActionButton(
                                        icon=ft.Icons.FILTER_LIST_ROUNDED,
                                        bgcolor= "#ffffff",
                                        # offset=ft.Offset(0,-0.5),
                                        on_click=toggle_filter
                                    )
                                ]
                            ),
                        )
                    ]   
                )
            )
        ],
    )


def update_wildex_region_section():
    cards = []

    return ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=180,
            child_aspect_ratio=0.85,
            spacing=8,
            run_spacing=8,
            controls= cards,
        )

def build_region_list_filter_button():

    menu_items = []

    for region in get_regions():

        menu_items.append(
            ft.Container(
                content = ft.Text(region.replace("_", " ").title()),
                data=region,
                bgcolor= "#292929",
                border_radius=8,
                padding=12,
                on_click=on_filter_region_selected
            )
        )



    return ft.ListView(
        controls=menu_items,
        spacing=5,
        auto_scroll=False,
        expand=True
    )

def build_card(region_name, wild):
    # print(region_name)
    return ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,

        on_tap= component.get_nav("on_card_click", [region_name, wild['id']]),
        content= ft.Container(
            bgcolor="#e1eeee",
            # border=ft.Border.all(2, "#A0E4E5"),
            border_radius=0,
            padding=5,

            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        alignment=ft.Alignment.CENTER,
                        padding=5,
                        content=component.build_hero(wild, 120, 110)
                    ),                        
                    ft.Text(
                        f"{wild['name']}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        color="#969595",
                        no_wrap=True,
                    ),
                ],
                spacing=1
            )
        )
    )

def on_filter_region_selected(e):
    region = e.control.data
    e.control.bgcolor = "#356859" if region in region_visible else "#292929"
    # print(is_selected)

    if region in region_visible:
        region_visible.remove(region)
    else:
        region_visible.append(region)
    
    # print(region_visible)
    for s in regions_sections:
        if not region_visible:
            s.visible = True
        elif s.data in region_visible:
            s.visible = True
        else:
            s.visible = False

    component.page.update()