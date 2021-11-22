import dash_bootstrap_components as dbc
import dash_core_components as dcc 
from dash import html

def create_card(title, description, image_ref_id):
   card = dcc.Link(dbc.Card(
      [
         dbc.CardImg(src=f"../static/images/sample{str(image_ref_id)}.jpg", top=True),
         dbc.CardBody(
               [
                  html.H4(title, className="card-title"),
                  html.P(
                     description,
                     "make up the bulk of the card's content.",
                     className="card-text",
                  ),
                  dbc.Button("Go somewhere", color="primary"),
               ]
         ),
      ],
   
   ), href=f"/sample{str(image_ref_id)}", style={
      "text-decoration": "none",
       "color": "black", 
       })

   return html.Div([card], style={"justify-content": "space-between"})