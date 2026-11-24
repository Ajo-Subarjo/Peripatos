import flet as ft


page: ft.Page


def card_tag(region_name, wild_id):
     return f"card-{region_name}-{wild_id}"



def build_image(region_name, wild, sizeX, sizeY = None):
    id = wild['id']
    
    if sizeY == None:
        sizeY = sizeX


    return ft.Container(
        content= ft.Container(
            width=sizeX,
            height=sizeY,
            alignment=ft.Alignment.CENTER,
            border_radius=0,
            content=ft.Image(
                src=(f"wild_image/{region_name}/{id}.jpg"),
                gapless_playback=True,
                width=sizeX,
                height=sizeY,
                fit=ft.BoxFit.COVER
            ),
        )
    )






def extract_data(route):
        parts = route.strip("/").split("/") 

        if len(parts) == 3 and parts[0] == "Wildex":
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
            print("go back")
            async def go_back(e):
               await page.push_route("/Wildex")

            return go_back


async def open_card(data):
    await page.push_route(f"/Wildex/{data[0]}/{data[1]}")

def build_navbar():

    return ft.Container(
        bgcolor="#ffffff",
        
        height=70,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Container(
                    border_radius=1,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.PHOTO_ALBUM_SHARP,
                                color="#356859",
                                size=36
                            )
                        ]
                    )
                ),
                ft.Container(
                    width=128,
                    height=72,
                    alignment=ft.Alignment.TOP_CENTER,
                    border_radius=32,
                    offset=ft.Offset(0, -0.35),
                    bgcolor="#c5dad4",
                    content=ft.Icon(
                        ft.Icons.CAMERA_ENHANCE,
                        color="#356859",
                        size=64,
                    ),

                    on_click=lambda e: print("GO TO CAMERA")
                    
                ),
                ft.Container(
                    border_radius=1,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.BOOK_SHARP,
                                color="#356859",
                                size=36
                            )
                        ]
                    )
                )
            ]
        )
    )



