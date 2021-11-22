import dash 
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd 
import numpy as np 
import json 
import os 
import datetime 
import time 
import uuid 
import requests

from api.get_data import request_api 
from api.get_vector import get_vector
from components.nav import create_navbar
from components.card import create_card
from components.table import create_table, create_modal
from components.pagenation import create_pagenation
from db import request_post_db

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions = True)
server = app.server

uid = str(uuid.uuid4())
request_post_db(uid, "/", "")
# 昨日以降の履歴を削除する
today = str(datetime.datetime.today()).split()[0]
for file in os.listdir("data/vector"):
    if file.find(".csv") >= 0:
        if today not in file.split(".")[0]:
            os.remove(f"data/vector/{file}")

for file in os.listdir("data/raw"):
    if file.find(".csv") >= 0:
        if today not in file.split(".")[0]:
            os.remove(f"data/raw/{file}")

config = {
    "YEAR": [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021], 
    "DEBUG": False, 
    "ROOT_URL": "http://api.moemoe.tokyo/anime/v1/master/", 
    "WEB_HOOK_URL": "https://hooks.slack.com/services/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",
    "year": 0, 
    "season": 0, 
    "sex": None,
    "kwd": None,
    "data": None,
    "select_data": None,
    "contact": {
        "email": "", 
        "question": "",
    }
}

if config["DEBUG"]:
    df = pd.read_csv("./data/raw/sample.csv")
    config["data"] = df 
else:
    files = os.listdir("data/raw")
    files = [file.split(".")[0] for file in files]
    if today not in files:
        df = request_api(config)
        config["data"] = df 
        df.to_csv(f"data/raw/{today}.csv", index=False)
    else:
        df = pd.read_csv(f"data/raw/{today}.csv")
        config["data"] = df 
    

# 年別検索の入力
year_input = dbc.Form([dbc.Label("年別", html_for="select-year", width=2),
    dbc.Select(
                    id="select-year", 
    options=[
        {"label": year, "value": year} for year in config["YEAR"]
    ]
)])#end formgroup

season_input = dbc.Form([dbc.Label("季節", html_for="select_season", width=2), 
                              dbc.Select(
                    id="select-season", 
    options=[
        {"label": "冬", "value": 1},
        {"label": "春", "value": 2},
        {"label": "夏", "value": 3},
        {"label": "秋", "value": 4},
    ]
)])#end formgroup

# 人気検索の入力
radioitems = dbc.Form(
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
kwd_input = dbc.Form([dbc.Label("キーワード", html_for="input-kwd", width=2)
                    , dbc.Input(type="text"
                                        , id="input-kwd"
                                        , placeholder="ワンピース") #end input
                        ])#end formgroup


kwd_input_ = dbc.Form([dbc.Label("キーワード", html_for="input-kwd_", width=2)
                    , dbc.Input(type="text"
                                        , id="input-kwd_"
                                        , placeholder="ワンピース") #end input
                        ])#end formgroup

# 最初のページのビュー
index_page = html.Div([
    create_navbar(),
    dbc.Carousel(
    items=[
        {
            "key": "1",
            "src": "static/images/sample001.jpg",
            "header": "With header ",
            "caption": "and caption",
        },
        {
            "key": "2",
            "src": "static/images/sample002.jpg",
            "header": "With header only",
            "caption": "",
        },
        {
            "key": "3",
            "src": "static/images/sample003.jpg",
            "header": "",
            "caption": "This slide has a caption only",
        },
        {
            "key": "4",
            "src": "static/images/sample004.jpg",
            "header": "",
            "caption": "This slide has a caption only",
        },

    ],
    controls=False,
    indicators=False,
    interval=2000,
    ride="carousel"), 
    dbc.Container([
        html.Div([
            html.Hr(style={"width": "20%", "margin": "auto"}),
            html.H2("分析", className="mt-3"),  

        ], style={"text-align": "center"}, className="mb-6"),
        html.Div([
            # html.Div([
                create_card(
                    "放送日から検索", 
                    "年と季節から該当するアニメ放送日のデータを取得します。", 
                    "001"), 
                create_card(
                    "人気のアニメ検索", 
                    "性別から過去から最も人気の高いアニメをピックアップします。", 
                    "002"),    
            # ])
        
        ], style={"display": "flex", "margin": "auto"}), 
        html.Div([
            # html.Div([
            create_card(
                "キーワード検索", 
                "キーワードを入力してマッチしたアニメを取得します。", 
                "003"), 
            create_card(
                "アニメ推薦システム", 
                "キーワードから類似したアニメを推薦します。おススメが高い順で並び替えます。", 
                "004"),    
        # ])
        
        ], style={"display": "flex", "margin": "auto"})
    ], style={"margin-top": "70px"})
])

# 検索ページのビュー
def build_sample001_page():
    return html.Div([
        create_navbar(),
        dbc.Container([
            html.Div([
            html.H2("放送された時期から検索"),
            html.P("時系列からデータを取得します。"),
            dbc.Card(dbc.CardBody([
                dbc.Form([year_input, season_input]),
                dbc.Button("検索する", id="load-year", n_clicks=0),
            ])), 
            dbc.Spinner(html.Div(id="load-year-text", children=[
                dbc.Alert("入力してください", color="primary")
            ])),
            html.Div("", id="dummy")
            ]), 
        ])
    ])

def build_sample002_page():
    return html.Div([
        create_navbar(),
        dbc.Container([
            html.Div([
            html.H2("性別ごとに人気のアニメを検索"), 
            html.P("放映されたシーズン数が多い順にアニメ名を取得します。"),
            dbc.Card(dbc.CardBody([dbc.Form([radioitems]), 
                dbc.Button("検索する", id="load-pop", n_clicks=0),
            ])), 
            dbc.Spinner(html.Div(id="load-pop-text", children=[
                dbc.Alert("入力してください", color="primary")
            ])),
            html.Div("", id="dummy1")
        ]), 
        ])
    ])

def build_sample003_page():
    return html.Div([
        create_navbar(),
        dbc.Container([
            html.Div([
            html.H2("キーワード検索"), 
            html.P("単語にマッチしたアニメを調べます。"),
            dbc.Card(dbc.CardBody([dbc.Form([kwd_input]), 
                dbc.Button("検索する", id="load-kwd", n_clicks=0),
            ])), 
            dbc.Spinner(html.Div(id="load-kwd-text", children=[
                dbc.Alert("入力してください", color="primary")
            ])),
            html.Div("", id="dummy2")
        ]), 
        ])
    ])

def build_sample004_page():
    return html.Div([
        create_navbar(),
        dbc.Container([
            html.Div([
            html.H2("キーワードから推薦"),
            html.P("機械学習を使って、似たアニメを調べます。スタート時に遅延が発生する可能性があります。"),
            dbc.Card(dbc.CardBody([dbc.Form([kwd_input_]),
                dbc.Button("検索する", id="load-rcd", n_clicks=0),
            ])), 
            dbc.Spinner(html.Div(id="load-rcd-text", children=[
                dbc.Alert("入力してください", color="primary")
            ])),
            html.Div("", id="dummy3")
        ]), 
        ])
    ])

def build_contact_page():
    email_input = html.Div(
        [
            dbc.Label("Email"),
            dbc.Input(id="email-input", type="email", value="", placeholder="Enter Email", ),
            dbc.FormText("We only accept gmail..."),
            dbc.FormFeedback("That looks like a gmail address :-)", type="valid"),
            dbc.FormFeedback(
                "Sorry, we only accept gmail for some reason...",
                type="invalid",
            ),
        ]
    )

    password_input = html.Div(
        [  
            dbc.Label("About Question", html_for="example-password"),
            dbc.Input(
                type="text",
                id="example-password",
                placeholder="Enter Questions",
            ),
            dbc.FormText(
                "問い合わせ内容について", color="secondary"
            ),
        ],
        className="mb-3",
    )

    form = dbc.Form([email_input, password_input, create_modal()])
    return html.Div([
        create_navbar(), 
        dbc.Container([
            form,
            html.Div("", id="dummy-form1"),
            html.Div("", id="dummy-form1"),
        ])
    ])

@app.callback(
    [Output("dummy-form1", "value")], 
    [Input("email-input", "value"), Input("example-password", "value")]
)
def register_content_about_contact(email, question):
    if(email is not None) and (question is not None):
        config["contact"]["email"] = email 
        config["contact"]["question"] = question 

        return [html.Div()]
    return [html.Div()]


@app.callback(
    [Output("email-input", "valid"), Output("email-input", "invalid")],
    [Input("email-input", "value")],
)
def check_validity(text):
    if text:
        is_gmail = text.endswith("@gmail.com")
        return is_gmail, not is_gmail
    return False, False

# 検索ボタンのイベント
@app.callback([Output("dummy", "value")], 
             [Input("select-year", "value"), 
             Input("select-season", "value")])
def update_select_btn(year, season):
    if(year is not None) and (season is not None):
        time.sleep(3)
        config["year"] = int(year)
        config["season"] = int(season)

        return [html.Div()]
    return [html.Div()]

@app.callback(
    Output("load-year-text", "children"), [Input("load-year", "n_clicks")]
)
def load_output_year_and_season(n):
    try:
        if n and config["year"] != 0 and config["season"] != 0:  
            time.sleep(2)
            return [dbc.Alert([
                dcc.Link(f"{config['year']}で検索する", href=f"/search?year={config['year']}&season={config['season']}")
            ], color="primary")]

    except Exception as e:
        return [dbc.Alert("存在しません", color="danger")]
    return [dbc.Alert("入力してください", color="primary")]
        
 
    
@app.callback([Output("dummy1", "children")], 
             [Input("radioitems-input", "value")])
def update_radio_btn(sex):
    if(sex is not None):
        time.sleep(2)
        config["sex"] = sex 

        return [html.Div()]
    return [html.Div()]
@app.callback(
    Output("load-pop-text", "children"), [Input("load-pop", "n_clicks")]
)
def load_output_population(n):
    try:
        if n and config["sex"] is not None:  
            time.sleep(2)
            return [dbc.Alert([
                dcc.Link("検索する", href=f"/rank?gender={config['sex']}")
            ], color="primary")]

    except Exception as e:
        return [dbc.Alert("存在しません", color="danger")]
    return [dbc.Alert("入力してください", color="primary")]

    
@app.callback([Output("dummy2", "children")], 
             [Input("input-kwd", "value")])
def update_input_kwd(kwd):
    if(kwd is not None):
        time.sleep(2)
        config["kwd"] = kwd

        return [html.Div()]
    return [html.Div()]

@app.callback(
    Output("load-kwd-text", "children"), [Input("load-kwd", "n_clicks")]
)
def load_output_keyword(n):
    try:
        if n and config["kwd"] is not None:  
            time.sleep(2)
            df = config["data"]
            if df[df.title.str.contains(config["kwd"])].shape[0] == 0:
                raise ValueError("Not Found")
            else:
                return [dbc.Alert([
                    dcc.Link("検索する", href=f"/input?keyword={config['kwd']}")
                ], color="primary")]

    except Exception as e:
        return [dbc.Alert("存在しません", color="danger")]
    return [dbc.Alert("入力してください", color="primary")]

   
        
        
@app.callback([Output("dummy3", "children")], 
             [Input("input-kwd_", "value")])
def update_input_kwd(kwd):
    if(kwd is not None):
        time.sleep(2)
        config["kwd"] = kwd

        return [html.Div()]
    return [html.Div()]
@app.callback(
    Output("load-rcd-text", "children"), [Input("load-rcd", "n_clicks")]
)
def load_output_recommendation(n):
    try:
        if n and config["kwd"] is not None:  
            time.sleep(2)
            df = config["data"]
            if df[df.title.str.contains(config["kwd"])].shape[0] == 0:
                raise ValueError("Not Found")
            else:
                return [dbc.Alert([
                    dcc.Link("推薦する", href=f"/recommend?keyword={config['kwd']}")
                ], color="primary")]

    except Exception as e:
        return [dbc.Alert("存在しません", color="danger")]
    return [dbc.Alert("入力してください", color="primary")]




def build_main_page():
    df = config["data"]
    year = config["year"]
    season = config["season"]
    request_post_db(uid, "/search", str(year) + "-" + str(season))
    dfs = df[(df.year == year) & (df.season == season)]
    config["select_data"] = dfs 

    return html.Div([
        create_navbar(),
        dbc.Container([
            create_pagenation(dfs.shape[0] // 10),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_rank_page():
    df = config["data"]
    sex = config["sex"]
    request_post_db(uid, "/rank", str(sex))
    if sex == 0:
        dfs = df[df.sex == sex]
    elif sex == 1:
        dfs = df[df.sex == sex]
    else:
        dfs = df 
        
    popular = dfs.title_short1.value_counts(normalize=True).to_frame().sort_values("title_short1", ascending=False)
    dfs = pd.merge(dfs, popular, how="right", left_on="title_short1", right_index=True).reset_index(drop=True)[:21]
    config["select_data"] = dfs
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_pagenation(dfs.shape[0] // 10),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_kwd_page():
    kwd = config["kwd"]
    request_post_db(uid, "/input", kwd)
    dfs = df[df.title.str.contains(kwd)]
    config["select_data"] = dfs 
    return html.Div([
        create_navbar(),
        dbc.Container([
            create_pagenation(dfs.shape[0] // 10),
            dcc.Link("検索ページへ戻る", href="/")
        ]),
    ], style={"margin": "0px"})

def build_recommend_page():
    kwd = config["kwd"]
    request_post_db(uid, "/recommend", kwd)
    # 履歴があればそこから取得する
    today = str(datetime.datetime.today()).split()[0] 
    if today+".csv" not in os.listdir("./data/vector"):
        v = get_vector(config["data"])
        v["99999"] = v.index 
        v.to_csv(f"./data/vector/{today}.csv", index=False)
    else:
        v = pd.read_csv(f"./data/vector/{today}.csv")
        
    kwd_col = v.columns[v.columns.str.contains(str(kwd))][0]
    v = v[[kwd_col, "99999"]].sort_values(kwd_col, ascending=False).reset_index(drop=True)
    v.columns = ["recommend", "title"]
    v = v[v.recommend >= 0.75]
    dfs = pd.merge(config["data"], v, how="right", left_on="title", right_on="title")
    config["select_data"] = dfs 

    return html.Div([
        create_navbar(),
        dbc.Container([
            create_pagenation(dfs.shape[0] // 10),
            dcc.Link("検索ページへ戻る", href="/")
        ]), 
    ], style={"margin": "0px"})
    

# Root path 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], style={"font-weight": "bold"})
@app.callback(Output("page-content", "children"), 
             [Input("url", "pathname")])
def display_page(pathname):
    if pathname.find("/search") >= 0:
        return build_main_page() 
    elif pathname.find("sample001") >= 0:
        return build_sample001_page()
    elif pathname.find("sample002") >= 0:
        return build_sample002_page()
    elif pathname.find("sample003") >= 0:
        return build_sample003_page()
    elif pathname.find("sample004") >= 0:
        return build_sample004_page()
    elif pathname.find("/rank") >= 0:
        return build_rank_page()
    elif pathname.find("/input") >= 0:
        return build_kwd_page()
    elif pathname.find("/recommend") >= 0:
        return build_recommend_page()
    elif pathname.find("/github") >= 0:
        return build_source_page()
    elif pathname.find("/document") >= 0:
        return build_document_page()
    elif pathname.find("/contact") >= 0:
        return build_contact_page()
    else:
        return index_page 


# コンタクトページのモーダル開閉
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if is_open is not True and config["contact"]["email"] != "" and config["contact"]["question"] != "":
        requests.post(config["WEB_HOOK_URL"], data=json.dumps({
            "username": "from_anime_analysis_page", 
            "text": f"email: {config['contact']['email']} \n text: {config['contact']['question']}\n"
        }))

        config["contact"]["email"] = ""
        config["contact"]["question"] = ""

        return not is_open 
    elif is_open:
        if n1 or n2:
            return not is_open 

@app.callback(
    Output("pagination-contents", "children"),
    [Input("pagination", "active_page")],
)
def change_page(page):
    df = config["select_data"]
    if page is None:
        page = 1
    if page:
        return create_table(df.iloc[page * 10 - 10: page * 10])
    return "Not Found 404"

if __name__ == "__main__":
    app.run_server(debug=True)