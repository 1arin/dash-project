import dash 
from dash import Dash, html, dcc,callback,Output,Input
import plotly.express as px
import pandas as pd 
from datetime import date

df = pd.read_csv('nst.csv')
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Air Quality Dashboard'),
        dcc.DatePickerRange(
        month_format='MMM D YY',
        end_date_placeholder_text='MMM D YY',
        start_date=date(2024, 1, 1)
        ),
        dcc.Dropdown(
            id='parameter',
            options=['PM2.5', 'PM10','O3','CO', 'NO2', 'SO2'],
            value='PM2.5'
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
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    fig = px.line(filtered_df, x='Date', y=['PM25', 'PM10', 'O3', 'CO', 'NO2', 'SO2'], title='Air Quality')
    return fig

if __name__ =='__main__':
    app.run(debug=True)