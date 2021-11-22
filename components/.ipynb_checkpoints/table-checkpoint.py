import pandas as pd 
import numpy as np 
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
import uuid 

def generate_card(df, recommend):
    ids = str(uuid.uuid4())[:4]

    if recommend:
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(df["title"], className=f"card-title-{ids}"),
                    html.H5(f"オススメ度 {round(df['recommend'] * 100.0, 1)} %"), 
                    html.P(df["title_short1"], className=f"card-subtitle-{ids}"),
                    dbc.CardLink("公式サイトへ", href=df["public_url"]),
                ]
            ),
            style={"width": "18rem"},
        )
    else:
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(df["title"], className=f"card-title-{ids}"),
                    html.P(df["title_short1"], className=f"card-subtitle-{ids}"),
                    dbc.CardLink("公式サイトへ", href=df["public_url"]),
                ]
            ),
            style={"width": "18rem"},
        )
    return card

def generate_table(df, recommend):
    df = df.reset_index(drop=True)
    columns = df.columns
    
    return html.Div([
        html.Div([
            generate_card(df.iloc[0], recommend)
        ], style={"justify-content": "space-between", "width": "33.3%"}),
        html.Div([
            generate_card(df.iloc[1], recommend)
        ], style={"justify-content": "space-between", "width": "33.3%"}),
        html.Div([
            generate_card(df.iloc[2], recommend)
        ], style={"justify-content": "space-between", "width": "33.3%"}),
    ], style={"display": "flex", "width": "100%", "margin-top": "20px"})
#     return dbc.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in columns])
#         ), 
#         html.Tbody([
#             html.Tr([
#                 html.Td(df.iloc[i][col]) for col in columns
#             ]) for i in range(df.shape[0])
#         ])
#     ], bordered=True, dark=True, hover=True, responsive=True, striped=True)


def create_table(df, recommend=False):
    length = df.shape[0]
    
    if recommend:
        df = df[["title", "title_short1", "public_url", "recommend"]]
    else:
        df = df[["title", "title_short1", "public_url"]]
        
    
    if length < 3:
        return html.Div([
            html.H1(f"[{length}]件見つかりました"),
            html.Div([generate_card(df.iloc[i], recommend) for i in range(length)])
        ])
    else:
    
        return html.Div([
            html.Div([
                html.H1(f"[{length}]件見つかりました。"), 
                html.Div([generate_table(df.iloc[3*i:3*i+3], recommend) for i in range(df.shape[0] // 3)])

            ])
        ])