import flet as ft


WILDEX = {
    "west_java": [
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

}




def hero_tag(wild_id):
    return f"bio-hero-{wild_id}"


def main(page: ft.Page):

    region_visible = []


    page.title = "Biodex"


    def extract_data(route):
        parts = route.strip("/").split("/") 

        if len(parts) == 3 and parts[0] == "wild":
            try:
                return [parts[1], int(parts[2])]
            except ValueError:
                pass
        return None

    def wild_by_id(region, wid):
        return next(
            (w for w in WILDEX.get(region, []) if w["id"] == wid),
            None,
        )    

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
                    src=(f"wild_image/west_java/{id}.jpg"),
                    width=sizeX,
                    height=sizeY,
                    fit=ft.BoxFit.COVER
                ),
            )
        )

    def build_card(region_name, wild):
        print(region_name)
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            data = wild,

            on_tap= get_nav("on_card_click", [region_name, wild['id']]),
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
        region, is_selected = e.control.data
        print(is_selected)

        if not is_selected:
            region_visible.append(region)
        else:
            region_visible.remove(region)

        # print(region_visible)

        refresh_page()



    def build_wildex_view():

        regions_sections = []

        filter_box = ft.Container(
            visible=False,
            padding=8,

            border_radius=8,
            bgcolor="#Ffffff",

            content=ft.Column(
                tight=True,
                height=min(len(WILDEX) * 50, 150),
                margin=ft.Margin(0,0,0,20),
                # scroll=ft.ScrollMode.AUTO,
                controls=[
                    build_region_list_filter(region_visible),
                ]
            )
        )

        def toggle_filter():
            filter_box.visible = not filter_box.visible
            print(filter_box.visible)
            page.update()

        
        for region_name, wilds in WILDEX.items():
            
            cards = []

            if len(region_visible) != 0 and region_name not in region_visible:
                print(len(region_visible))
                continue

            for wild in wilds:
                cards.append(build_card(region_name, wild)) 


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


    def build_region_list_filter(region_visible):

        menu_items = []

        for region in WILDEX:

            if region in region_visible:
                is_selected = True
            else:
                is_selected = False

            menu_items.append(
                ft.Container(
                    content = ft.Text(region.title()),
                    bgcolor="#356859" if is_selected else "#292929",
                    data=(region, is_selected),
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



    def build_detail_view(data):
        region_name = data[0]
        wild = data[1]
        print(f"/wild/{region_name}/{wild['id']}")
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



    def get_nav(name, data = []):

        if name == "on_card_click":
            def on_card_click(e):
                page.run_task(open_card, data)
            
            return on_card_click

        elif name == "go_back":
            async def go_back(e):
               await page.push_route("/")

            return go_back

    async def open_card(data):
        await page.push_route(f"/wild/{data[0]}/{data[1]}")




    def refresh_page(e=None):
        page.views.clear()

        page.views.clear()
        page.views.append(build_wildex_view())
              

        print(page.route)
        result = extract_data(page.route)

        if result is not None:
            region, wid = result
            wild = wild_by_id(region, wid)

            if wild:
                page.views.append(build_detail_view([region, wild]))

        page.update()


    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)

            await page.push_route(
                page.views[-1].route
            )

    page.on_route_change = refresh_page
    page.on_view_pop = view_pop

    refresh_page()

if __name__ == "__main__":
    ft.run(main)

