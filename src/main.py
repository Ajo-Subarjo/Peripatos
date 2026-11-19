import flet as ft


WILDEX = {
    "west java": [
        {
            "id": 650,
            "name": "Chespin",
            "type": "Grass",
            "height": "0.4 m",
            "weight": "9.0 kg",
            "description": "A grass Type Pokemon With a Tough shell covering its head"
        },
        {
            "id": 650,
            "name": "Quilladin",
            "type": "Grass",
            "height": "0.7 m",
            "weight": "29.0 kg",
            "description": "A Grass-type Pokémon."
        },
    ],

    "east java": [
        {
            "id": 650,
            "name": "Chesnaught",
            "type": "Grass/Fighting",
            "height": "1.6 m",
            "weight": "90.0 kg",
            "description": "A Grass-type Pokémon."
        }
    ]
}

region_visible = ""



def hero_tag(wild_id):
    return f"bio-hero-{wild_id}"


def main(page: ft.Page):
    page.title = "Biodex"

    def wild_by_id(pid):
        return next(
            (p for p in WILDEX["west-java"] if p["id"] == pid),
            None
        )

    def route_wild_id(route):
        parts = route.strip("/").split("/") 

        if len(parts) == 2 and parts[0] == "wild":
            try:
                return int(parts[1])
            except ValueError:
                pass
        return None


    

    def build_hero(wild, sizeX, sizeY = None):
        id = wild['id']
        if sizeY == None:
            sizeY = sizeX
        return ft.Hero(
            tag=hero_tag(id),
            transition_on_user_gestures= True,
            content= ft.Container(
                width=sizeX,
                height=sizeY,
                alignment=ft.Alignment.CENTER,
                border_radius=0,
                content=ft.Image(
                    src=(f"wild_image/west-java/{id}.jpg"),
                    width=sizeX,
                    height=sizeY,
                    fit=ft.BoxFit.COVER
                ),
            )
        )

    def build_card(wild):
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,

            on_tap= get_nav("on_card_click", wild['id']),
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
                            content=build_hero(wild, 120, 110)
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
        region_visible = e.control.data
        # print(region_visible)



    def build_wildex_view():

        regions_sections = []
        region_names = []
        
        for region_name, wilds in WILDEX.items():
            
            cards = []

            if region_visible == "":
                for wild in wilds:
                    cards.append(build_card(wild))
            


            region_names.append(
                ft.PopupMenuItem(
                    region_name,
                    data=region_name,
                    on_click=on_filter_region_selected
                )
            )


            regions_sections.append(
                ft.Column(
                    controls=[
                        ft.Text(
                            region_name.replace("-", " ").title(),
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
                            ft.PopupMenuButton(
                                icon=ft.Icons.FILTER_LIST,
                                menu_position=ft.PopupMenuPosition.OVER,
                                items=region_names,
                                right=20,
                                bottom=20
                            ),
                        ]

                    )
                )
            ],
        )


    def build_detail_view(wild):
        return ft.View(
            route=f"/wild/{wild['id']}",
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
                            build_hero(wild, 400, 220),
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
                                on_click= get_nav("go_back"),
                            )
                        ],
                    ),
                ),
            ],
        )



    def get_nav(name, data = None):

        if name == "on_card_click":
            def on_card_click(e):
                page.run_task(open_card, data)
            
            return on_card_click

        elif name == "go_back":
            async def go_back(e):
               await page.push_route("/")

            return go_back

    async def open_card(wid):
        await page.push_route(f"/wild/{wid}")




    def route_change(e=None):
        page.views.clear()

        page.views.append(build_wildex_view())

        wid = route_wild_id(page.route)

        if wid is not None:
            wild = wild_by_id(wid)

            if wild:
                page.views.append(build_detail_view(wild))

        page.update()


    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)

            await page.push_route(
                page.views[-1].route
            )

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()

if __name__ == "__main__":
    ft.run(main)

