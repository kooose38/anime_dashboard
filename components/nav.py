import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.NavbarSimple(
                brand="Anime Analysis Platform",
                brand_href="/",
                color="primary",
                dark=True,
                sticky="top"
            )