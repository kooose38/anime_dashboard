import pandas as pd 
import numpy as np 
import plotly.express as px 
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc

def generate_table(df):
    columns = df.columns
    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in columns])
        ), 
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in columns
            ]) for i in range(df.shape[0])
        ])
    ], bordered=True, dark=True, hover=True, responsive=True, striped=True)


def create_table(df):
    length = df.shape[0]
    usecols = ["title", "public_url", "sex", "sequel"]
    df = df[usecols]
    
    return html.Div([
        html.Div([
            html.H1(f"[{length}]件見つかりました。"), 
            generate_table(df)
        ])
    ])