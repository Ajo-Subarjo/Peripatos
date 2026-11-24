import flet as ft
import component
from DB import get_grouped, get_regions

region_visible = []
regions_sections = []
is_filter_list_open = False

def build_wildex_view():

    component.page.views.clear()
    
    grouped = get_grouped()

    filter_box = ft.Container(
        padding=8,

        border_radius=8,
        bgcolor="#Ffffff",

        opacity=0,
        scale=0,
        animate_opacity=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT_SINE),
        animate_scale=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT_SINE),

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
        global is_filter_list_open
        is_filter_list_open = not is_filter_list_open
        # print(filter_box.visible)

        filter_box.opacity = 1 if is_filter_list_open else 0
        filter_box.scale =ft.Scale(scale=1 if is_filter_list_open else 0, alignment=ft.Alignment.BOTTOM_RIGHT)

        component.page.update()

    regions_sections.clear()

    
    for region_name, wilds in grouped.items():
        
        cards = []


        for wild in wilds:
            cards.append(build_card(region_name, wild)) 


        regions_sections.append(
            ft.Column(
                margin= ft.Margin(0,15,0,0),
                data=region_name,
                controls=[
                    ft.Text(
                        region_name.replace("_", " ").title(),
                        size=16,
                        color="#3E3A34",
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.GridView(
                        expand=True,
                        runs_count=3,
                        max_extent=180,
                        child_aspect_ratio=0.93,
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
            bgcolor="#356859",
            color="#e1eeee",
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
            content= ft.Hero(
                tag=component.card_tag(region_name, wild['id']),
                transition_on_user_gestures=True,
                content=ft.Container(
                    bgcolor="#e1eeee",
                    # border=ft.Border.all(2, "#A0E4E5"),
                    padding=8,
                    border_radius=5,
                    shadow=ft.BoxShadow(
                        blur_radius=3,
                        spread_radius=2,
                        color="#afc2bc",
                        offset=ft.Offset(5, 4),
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=component.build_image(region_name,wild, 130, 100)
                            ),                        
                            ft.Text(
                                f"{wild['name']}",
                                margin=ft.Margin.only(top=2),
                                size=16,
                                text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                color="#483B46",
                                no_wrap=True,
                            ),
                        ],
                        spacing=1
                    )
                )
            )
    )

def on_filter_region_selected(e):
    region = e.control.data
    # print(is_selected)

    if region in region_visible:
        region_visible.remove(region)
    else:
        region_visible.append(region)

    e.control.bgcolor = "#356859" if region in region_visible else "#292929"
    
    # print(region_visible)
    for s in regions_sections:
        if not region_visible:
            s.visible = True
        elif s.data in region_visible:
            s.visible = True
        else:
            s.visible = False

    component.page.update()