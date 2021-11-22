import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

def create_navbar():
    navbar = dbc.Navbar(
    dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("Anime Analysis Platform", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                 dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More", header=True),
                        dbc.DropdownMenuItem("UI source code", href="/github"),
                        dbc.DropdownMenuItem("about dataset", href="/document_dataset"),
                        dbc.DropdownMenuItem("contact", href="/contact"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                    color="white",
                    # style={"color": "white"}
                ),
            ]
        ),
        color="primary",
        dark=True,
        sticky="top"
    )
    return navbar