import flet as ft
import component
import router
from DB import init_db

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




def main(_page: ft.Page):

    init_db()

    component.page = _page
    page = component.page

    page.title = "Biodex"

    page.on_route_change = router.refresh_page
    page.on_view_pop = router.view_pop

    router.refresh_page(page)

if __name__ == "__main__":
    ft.run(main)

