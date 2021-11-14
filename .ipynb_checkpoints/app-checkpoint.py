import dash 
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go
import argparse 
import os 
import datetime 
import time 

from api.get_data import request_api 
from api.get_vector import get_vector
from components.nav import create_navbar
from components.table import create_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True)
server = app.server

config = {
    "YEAR": [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021], 
    "DEBUG": True, 
    "ROOT_URL": "http://api.moemoe.tokyo/anime/v1/master/", 
    "year": 0, 
    "season": 0, 
    "data": pd.read_csv("./data/raw/sample.csv")
}

if config:
    df = pd.read_csv("./data/raw/sample.csv")
else:
    df = request_api(config)

# 年別検索の入力
year_input = dbc.FormGroup([dbc.Label("年別", html_for="select-year", width=2),
    dbc.Select(
                    id="select-year", 
    options=[
        {"label": year, "value": year} for year in config["YEAR"]
    ]
)], row=True)#end formgroup

season_input = dbc.FormGroup([dbc.Label("季節", html_for="select_season", width=2), 
                              dbc.Select(
                    id="select-season", 
    options=[
        {"label": "冬", "value": 1},
        {"label": "春", "value": 2},
        {"label": "夏", "value": 3},
        {"label": "秋", "value": 4},
    ]
)], row=True)#end formgroup

# 人気検索の入力
radioitems = dbc.FormGroup(
    [
        dbc.Label("性別"),
        dbc.RadioItems(
            options=[
                {"label": "男性", "value": 0},
                {"label": "女性", "value": 1},
                {"label": "全て", "value": 2},
            ],
            value=2,
            id="radioitems-input",
        ),
    ]
)

# キーワード検索の入力
kwd_input = dbc.FormGroup([dbc.Label("キーワード", html_for="input-kwd", width=2)
                    , dbc.Input(type="text"
                                        , id="input-kwd"
                                        , placeholder="ワンピース") #end input
                        ], row=True)#end formgroup


kwd_input_ = dbc.FormGroup([dbc.Label("キーワード", html_for="input-kwd_", width=2)
                    , dbc.Input(type="text"
                                        , id="input-kwd_"
                                        , placeholder="ワンピース") #end input
                        ], row=True)#end formgroup


index_page = html.Div([
    create_navbar(),
    dbc.Container([
        html.Div([
            html.P("Anime API からデータを取得し、並び替え検索をします。"),
            html.P("非公式に公開されているデータベースから取得しています。"),
            html.P("使用したデータについて"),
            html.A("・Qiita", href="https://qiita.com/AKB428/items/64938febfd4dcf6ea698#get-animev1mastercours"),
            html.Br(),
            html.A("・Github", href="https://github.com/Project-ShangriLa/sora-playframework-scala"),
            html.Br(),
            html.P("UI開発者のソースコード"),
            html.A("・Github", href="https://github.com/kooose38/anime_dashboard"),
        ], style={"margin": "20px 0px"}), 
        html.Br(),
        html.Div([
            html.H2("放送された時期から検索"),
            html.P("時系列からデータを取得します。"),
            dbc.Card(dbc.CardBody([dbc.Form([year_input, season_input])])), 
            html.Div(id="div-btn-year", children=[
                dbc.Alert("入力してください", color="primary")
            ])
        ]), 
        html.Div([
            html.H2("性別ごとに人気のアニメを検索"), 
            html.P("放映されたシーズン数が多い順にアニメ名を取得します。"),
            dbc.Card(dbc.CardBody([dbc.Form([radioitems])])), 
            html.Div(id="div-btn-pop", children=[
                dbc.Alert("入力してください", color="primary")
            ])
        ]), 
        html.Div([
            html.H2("キーワード検索"), 
            html.P("単語にマッチしたアニメを調べます。"),
            dbc.Card(dbc.CardBody([dbc.Form([kwd_input])])), 
            html.Div(id="div-btn-kwd", children=[
                dbc.Alert("入力してください", color="primary")
            ])
        ]), 
        html.Div([
            html.H2("キーワードから推薦してもらう"),
            html.P("機械学習を使って、似たアニメを調べます。スタート時に遅延が発生する可能性があります。"),
            dbc.Card(dbc.CardBody([dbc.Form([kwd_input_])])), 
            html.Div(id="div-btn-recommend", children=[
                dbc.Alert("入力してください", color="primary")
            ])
        ]), 
    ])
], style={"margin": "0px", "height": "500px"})

@app.callback([Output("div-btn-year", "children")], 
             [Input("select-year", "value"), 
             Input("select-season", "value")])
def update_select_btn(year, season):
    if(year is not None) and (season is not None):
        time.sleep(3)
        config["year"] = int(year)
        config["season"] = int(season)
        
        try:
            return [dbc.Alert([
                dcc.Link(f"{year}年で検索する", href=f"/search?year={year}&season={season}")
            ], color="primary")]
        except Exception as e:
            return [dbc.Alert("存在しません", color="danger")]
    else:
        return [dbc.Alert("入力してください", color="primary")]
    
@app.callback([Output("div-btn-pop", "children")], 
             [Input("radioitems-input", "value")])
def update_radio_btn(sex):
    if(sex is not None):
        time.sleep(2)
        config["sex"] = sex 
    try:
        return [dbc.Alert([
                dcc.Link(f"検索する", href=f"/rank?sex={sex}")
            ], color="primary")]
    except Exception as e:
        return [dbc.Alert("存在しません", color="danger")]
    else:
        return [dbc.Alert("入力してください", color="primary")]
    
@app.callback([Output("div-btn-kwd", "children")], 
             [Input("input-kwd", "value")])
def update_input_kwd(kwd):
    if(kwd is not None):
        time.sleep(2)
        config["kwd"] = kwd
        
        try:
            return [dbc.Alert([
                dcc.Link(f"{kwd}で検索する", href=f"/input?keyword={kwd}")
            ], color="primary")]
        except Exception as e:
            return [dbc.Alert("存在しません", color="danger")]
    else:
        return [dbc.Alert("入力してください", color="primary")]
        
        
@app.callback([Output("div-btn-recommend", "children")], 
             [Input("input-kwd_", "value")])
def update_input_kwd(kwd):
    if(kwd is not None):
        time.sleep(2)
        config["kwd"] = kwd
        
        try:
            return [dbc.Alert([
                dcc.Link(f"{kwd}で推薦する", href=f"/recommend?keyword={kwd}")
            ], color="primary")]
        except Exception as e:
            return [dbc.Alert("存在しません", color="danger")]
    else:
        return [dbc.Alert("入力してください", color="primary")]


def build_main_page():
    df = config["data"]
    year = config["year"]
    season = config["season"]
    dfs = df[(df.year == year) & (df.season == season)]
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_table(dfs, ["title", "sex", "sequel", "public_url"]),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_rank_page():
    df = config["data"]
    sex = config["sex"]
    if sex == 0:
        dfs = df[df.sex == sex]
    elif sex == 1:
        dfs = df[df.sex == sex]
    else:
        dfs = df 
        
    dfs = dfs.title_short1.value_counts(normalize=True).to_frame().sort_values("title_short1", ascending=False)[:20]
    dfs.columns = ["popular"]
    dfs["title"] = dfs.index
    dfs["popular"] = dfs.popular * 100.0
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_table(dfs, ["title", "popular"]),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_kwd_page():
    kwd = config["kwd"]
    dfs = df[df.title.str.contains(kwd)]
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_table(dfs, ["title", "sex", "sequel", "public_url"]),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_recommend_page():
    kwd = config["kwd"]
    # 履歴があればそこから取得する
    today = str(datetime.datetime.today()).split()[0]
    if today not in os.listdir("./data/vector"):
        v = get_vector(config["data"])
        v["99999"] = v.index 
        v.to_csv(f"./data/vector/{today}.csv", index=False)
    else:
        v = pd.read_csv(f"./data/vector/{today}.csv")
        
    kwd_col = v.columns[v.columns.str.contains(str(kwd))][0]
    v = v[[kwd_col, "99999"]].sort_values(kwd_col, ascending=False)[1:20]
    v.columns = ["おすすめ度", "アニメ名"]
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_table(v, ["アニメ名", "おすすめ度"]),
            dcc.Link("検索ページへ戻る", href="/")
        ]), 
    ], style={"margin": "0px"})
    

# Root path 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
@app.callback(Output("page-content", "children"), 
             [Input("url", "pathname")])
def display_page(pathname):
    if pathname.find("/search") >= 0:
        return build_main_page() 
    elif pathname.find("/rank") >= 0:
        return build_rank_page()
    elif pathname.find("/input") >= 0:
        return build_kwd_page()
    elif pathname.find("/recommend") >= 0:
        return build_recommend_page()
    else:
        return index_page 

if __name__ == "__main__":
    app.run_server(debug=True)