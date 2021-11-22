import pandas as pd 
import numpy as np 
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc

# page_array = {
#    1: [0, 10], 
#    2: [10, 20], 
#    3: [20, 30]
#    4: [30, 40],
#    5: [40, 50], 

# }

def create_pagenation(max_values):
   pagenation = html.Div(
      [
         html.Div(children=[], id="pagination-contents"),
         dbc.Pagination(id="pagination", max_value=max_values),
      ]
   )

   return pagenation