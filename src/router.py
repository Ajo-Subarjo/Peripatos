from DB import wild_by_id
from pages.wildex import build_wildex_view
from pages.detailview import build_detail_view

import component

def refresh_page(e=None):
    print("refresh, route =", component.page.route)
    component.page.views.clear()

    if not component.page.views:
        component.page.views.append(build_wildex_view())
            

    print(component.page.route)
    result = component.extract_data(component.page.route)

    del component.page.views[1:]
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