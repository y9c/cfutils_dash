#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 yech <yech1990@gmail.com>
#
# Distributed under terms of the MIT license.

"""
dash demo.

"""

import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = True

app.layout = html.Div(
    [
        html.H1(children="Dna Feature Viewer"),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {
                        "x": [1, 2, 3],
                        "y": [4, 1, 2],
                        "type": "bar",
                        "name": "SF",
                    },
                    {
                        "x": [1, 2, 3],
                        "y": [2, 4, 5],
                        "type": "bar",
                        "name": u"Montréal",
                    },
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
        dcc.Upload(
            id="upload-image",
            children=html.Div(
                [
                    "Drag and Drop or ",
                    html.A("Select Files"),
                    " of ",
                    html.B("Reference Sequnece(*.gb)"),
                ]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-image-upload"),
    ]
)


def parse_contents(contents, filename, date):
    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Img(src=contents),
            html.Hr(),
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )


@app.callback(
    Output("output-image-upload", "children"),
    [Input("upload-image", "contents")],
    [
        State("upload-image", "filename"),
        State("upload-image", "last_modified"),
    ],
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children


if __name__ == "__main__":
    app.run_server(debug=True)
