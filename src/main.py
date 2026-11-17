import flet as ft


WILDEX = [
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
        "name": "Chespin",
        "type": "Grass",
        "height": "0.4 m",
        "weight": "9.0 kg",
        "description": "A grass Type Pokemon With a Tough shell covering its head"
    }
]



def hero_tag(wild_id):
    return f"bio-hero-{wild_id}"


def main(page: ft.Page):
    page.title = "Biodex"

    def wild_by_id(pid):
        return next(
            (p for p in WILDEX if p["id"] == pid),
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


    

    def build_hero(wild, size):

        return ft.Hero(
            tag=hero_tag(wild["id"]),
            transition_on_user_gestures= True,
            content= ft.Container(
                width=size,
                height=size,
                alignment=ft.Alignment.CENTER,
                content=ft.Image(
                    src=("assets/icon.svg"),
                    width=size,
                    height=size,
                    fit=ft.BoxFit.CONTAIN
                ),
            )
        )

    def build_card(wild):
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,

            on_tap= get_nav("on_card_click", wild['id']),
            content= ft.Container(
                bgcolor="#58E4EE",
                border=ft.Border.all(2, "#B5F9FA"),
                border_radius=13,
                padding=5,

                content=ft.Column(
                    [
                        build_hero(wild, 90),
                        ft.Text(
                            f"{wild['id']:04}",
                            size=18,
                            color="#007FA9",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                )
            )
        )




    def build_wildex_view():

        cards = []

        for wild in WILDEX:
            cards.append(build_card(wild))

        grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=180,
            child_aspect_ratio=0.85,
            spacing=8,
            run_spacing=8,
            controls= cards,
        )

        return ft.View(
            route="/",
            appbar=ft.AppBar(
                title=ft.Text("WILDEX"),
            ),
            controls=[
                ft.SafeArea(
                    expand=True,
                    content=grid,
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
                        spacing=15,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[
                            ft.Container(height=10),
                            build_hero(wild, 240),

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

