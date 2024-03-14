import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import pandas as pd
from datetime import date

df = pd.read_csv('nst.csv')
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Air Quality Dashboard'),
    dcc.DatePickerRange(
        id='date-picker-range',
        month_format='MMM D YY',
        end_date_placeholder_text='MMM D YY',
        start_date=date(2024, 1, 1)
    ),
    dcc.Dropdown(
        id='parameter',
        options=[
            {'label': 'PM2.5', 'value': 'PM25'},
            {'label': 'PM10', 'value': 'PM10'},
            {'label': 'O3', 'value': 'O3'},
            {'label': 'CO', 'value': 'CO'},
            {'label': 'NO2', 'value': 'NO2'},
            {'label': 'SO2', 'value': 'SO2'}
        ],
        value='PM25'
    ),
    dcc.Graph(id='air-quality-graph')
])

@app.callback(
    Output('air-quality-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('parameter', 'value')]
)
def update_graph(start_date, end_date, parameter):
    filtered_df = df[(df['DATETIMEDATA'] >= start_date) & (df['DATETIMEDATA'] <= end_date)]
    trace = []
    for param in parameter:
        trace.append(go.Scatter(x=filtered_df['DATETIMEDATA'], y=filtered_df[param], mode='lines', name=param))
    layout = go.Layout(title='Air Quality', xaxis=dict(title='Date and Time'), yaxis=dict(title='Concentration'))
    return {'data': trace, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)


