from dash import Dash 
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("clean_data.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)
order = ['PM25','PM10','O3','CO','NO2','SO2','WS','TEMP','RH','WD']

PAGE_SIZE = 5

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Analysis and Prediction"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏳️‍🌈", className="header-emoji"),
                html.H1(
                    children="Air4thai Nakorn-Sri", className="header-title"
                ),
                html.P(
                    children="Analysis and Prediction from Air4thai",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="parameter-filter",
                            options=[
                                {"label": param, "value": param}
                                for param in ['PM25','PM10','O3','CO','NO2','SO2','WS','TEMP','RH','WD']
                            ],
                            value="PM25",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                            display_format='YYYY-MM-DD',
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="all-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3(children="Data Analysis", className="header-table colored-background"), 
                        dash_table.DataTable(
                            id="analysis",
                            columns=[{"name": i, "id": i} for i in order],
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action="custom",
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in order
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("all-chart", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_chart(parameter, start_date, end_date):
    mask = (data["DATETIMEDATA"] >= start_date) & (data["DATETIMEDATA"] <= end_date)
    filtered_data = data.loc[mask, :]
    all_figure = {
        "data": [
            {
                "x": filtered_data["DATETIMEDATA"],
                "y": filtered_data[parameter],
                "type": "lines",
                "hovertemplate": f"{parameter}: %{{y:.2f}}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{parameter}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Datetime", "fixedrange": True},
            "yaxis": {"title": parameter, "fixedrange": True},
            "colorway": ["#b8c9b4"],
        },
    }
    return all_figure

@app.callback(
    Output("analysis", "data"),
    [Input('analysis', "page_current"),
     Input('analysis', "page_size")]
)
def update_table(analysis_page_current, analysis_page_size):
    analysis_data = (data[order]
                     .iloc[analysis_page_current * analysis_page_size: 
                           (analysis_page_current + 1) * analysis_page_size]
                            .to_dict('records'))
    return analysis_data


if __name__ == "__main__":
    app.run_server(debug=True)
