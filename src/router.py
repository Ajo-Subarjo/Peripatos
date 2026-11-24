from DB import wild_by_id
from pages.wildex import build_wildex_view
from pages.detailview import build_detail_view

import component



home = None


def refresh_page(e=None):
    global home
    print("refresh, route =", component.page.route)
    page = component.page
    # component.page.views.clear()

    if home is None:
        home = build_wildex_view()         

    if not page.views or page.views[0] is not home:
        page.views.clear()
        page.views.append(home)

    del page.views[1:]

    result = component.extract_data(page.route)
    
    if result is not None:
        region, wid = result
        wild = wild_by_id(region, wid)

        if wild:
            component.page.views.append(build_detail_view([region, wild]))

    component.page.update()


async def view_pop(e):
    print("view_pop, view =", e.view.route if e.view else None)
    if e.view is not None:
        component.page.views.remove(e.view)

        await component.page.push_route(
            component.page.views[-1].route
        )