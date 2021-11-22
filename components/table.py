import pandas as pd 
import numpy as np 
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
import uuid 

def create_modal():
    # id = str(uuid.uuid4())[:4]
    
    modal = html.Div(
        [
            dbc.Button("送信する", id=f"open-centered", color="primary"),
            dbc.Modal(
                [
                    # dbc.ModalHeader(dbc.ModalTitle("Header"), close_button=True),
                    dbc.ModalBody([
                        html.P("送信が完了しました。")
                    ]),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id=f"close-centered",
                            className="ms-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id=f"modal-centered",
                centered=True,
                is_open=False,
            ),
        ]
    )

    return modal 

def generate_card(df):
    df = df.to_frame().T
    is_recommend = "recommend" in df.columns.tolist()
    if df["season"].values[0] == 1:
        season = "冬"
    elif df["season"].values[0] == 2:
        season = "春"
    elif df["season"].values[0] == 3:
        season = "夏"
    else:
        season = "秋"

    if is_recommend:
        card = dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src="../static/images/sample001.jpg",
                                    className="img-fluid rounded-start",
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(df.title, className="card-title"),
                                        html.P(f"放送年: {df['year'].values[0]}"),
                                        html.P(f"シーズン: {season}"),
                                        html.P(f"愛称: {df['title_short1'].values[0]}"),
                                        html.A(f"公式URL: {df['public_url'].values[0]}", href=df["public_url"].values[0]),
                                        html.P(
                                            f"おすすめ度: {df['recommend'].values[0]}",
                                            className="card-text",
                                        ),
                                        # geenrate_modal(df),
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3",
                style={"width": "100%", "box-shadow": "4px 4px 4px gray"},
            )
    else:
        card = dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src="../static/images/sample002.jpg",
                                    className="img-fluid rounded-start",
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(df.title, className="card-title"),
                                        html.P(f"放送年: {df['year'].values[0]}"),
                                        html.P(f"シーズン: {season}"),
                                        html.P(f"愛称: {df['title_short1'].values[0]}"),
                                        html.A(f"公式URL: {df['public_url'].values[0]}", href=df["public_url"].values[0]),
                                        # geenrate_modal(df),
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3",
                style={"width": "100%", "box-shadow": "4px 4px 4px gray"},
            )
    return card



def create_table(df):
    # length = df.shape[0]
    
    # if recommend:
    #     df = df[["title", "title_short1", "public_url", "recommend"]]
    # else:
    #     df = df[["title", "title_short1", "public_url"]]


    return html.Div([
        html.Div([generate_card(df.iloc[i]) for i in range(df.iloc[:10].shape[0])])
    ])


        
    
    # if length < 3:
    #     return html.Div([
    #         html.H1(f"[{length}]件見つかりました"),
    #         html.Div([generate_card(df.iloc[i], recommend) for i in range(length)])
    #     ])
    # else:
    
    #     return html.Div([
    #         html.Div([
    #             html.H1(f"[{length}]件見つかりました。"), 
    #             html.Div([generate_table(df.iloc[3*i:3*i+3], recommend) for i in range(df.shape[0] // 3)])

    #         ])
    #     ])