import flet as ft


page: ft.Page


def hero_tag(wild_id):
    return f"bio-hero-{wild_id}"


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

def extract_data(route):
        parts = route.strip("/").split("/") 

        if len(parts) == 3 and parts[0] == "wild":
            try:
                return [parts[1], int(parts[2])]
            except ValueError:
                pass
        return None



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


