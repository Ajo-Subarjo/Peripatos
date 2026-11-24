import flet as ft
import component
import router
from DB import init_db




def main(_page: ft.Page):

    init_db()

    component.page = _page
    page = component.page

    
    page.bgcolor="#c5dad4"

    page.theme = ft.Theme(
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.ZOOM,
            ios=ft.PageTransitionTheme.ZOOM,
            macos=ft.PageTransitionTheme.ZOOM,
            linux=ft.PageTransitionTheme.ZOOM,
            windows=ft.PageTransitionTheme.ZOOM,
        )
    )

    page.title = "Biodex"

    page.on_route_change = router.refresh_page
    page.on_view_pop = router.view_pop

    router.refresh_page(page)





if __name__ == "__main__":
    ft.run(main)


