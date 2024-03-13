@app.callback(
    Output("PM25-chart", "figure"),
    Output("PM10-chart", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ]
)

def update_chart_prediction(n_intervals):
    train = pd.read_csv('./datafile/train.csv')
    train['DATETIMEDATA'] = pd.to_datetime(train['DATETIMEDATA'])

    now = pd.Timestamp.now()
    start_date = now.date()
    end_date = start_date + pd.DateOffset(days=7)

    loaded_model_PM25 = load_model('PM25_pipeline')

    future_dates_PM25 = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_PM25 = pd.DataFrame({'DATETIMEDATA': future_dates_PM25})
    future_data_PM25['PM10'] = train['PM10'].mean().round(2)
    future_data_PM25['O3'] = train['O3'].mean().round(2)
    future_data_PM25['CO'] = train['CO'].mean().round(2)
    future_data_PM25['NO2'] = train['NO2'].mean().round(2)
    future_data_PM25['WS'] = train['WS'].mean().round(2)

    predictions_PM25 = predict_model(loaded_model_PM25, data=future_data_PM25)
    # predictions_PM25 = predictions_PM25.rename(columns={'Label': 'prediction_label'})
    # predictions_PM25['prediction_label'] = predictions_PM25['prediction_label'].round(2)

    PM25_chart_figure = {
        "data": [
            {
                "x": future_dates_PM25,
                "y": predictions_PM25['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM25 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': { 
                'text' : f'PM25 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM25 Forecast', "fixedrange": True},
            "colorway": ["#B5C0D0"],
        },
    }

    loaded_model_PM10 = load_model('PM10_pipeline')

    future_dates_PM10 = pd.date_range(start=start_date, end=end_date, freq='D')
    future_data_PM10 = pd.DataFrame({'DATETIMEDATA': future_dates_PM10})
    future_data_PM10['PM25'] = train['PM25'].mean().round(2)
    future_data_PM10['O3'] = train['O3'].mean().round(2)
    future_data_PM10['CO'] = train['CO'].mean().round(2)
    future_data_PM10['NO2'] = train['NO2'].mean().round(2)
    future_data_PM10['WS'] = train['WS'].mean().round(2)

    predictions_PM10 = predict_model(loaded_model_PM10, data=future_data_PM10)
    # predictions_PM10 = predictions_PM10.rename(columns={'Label': 'prediction_label'})
    # predictions_PM10['prediction_label'] = predictions_PM10['prediction_label'].round(2)

    PM10_chart_figure = {
        "data": [
            {
                "x": future_dates_PM10,
                "y": predictions_PM10['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM10 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': { 
                'text' : f'PM10 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM10 Forecast', "fixedrange": True},
            "colorway": ["#ccc1b7"],
        },
    }

    return PM25_chart_figure , PM10_chart_figure 

table_predict = pd.read_csv('./datafile/merged_table_PM10_PM25_prediction.csv')

@app.callback(
    Output("prediction", "data"),
    [
        Input('interval-component', 'n_intervals')
    ]
)
def update_table(n_intervals):
    prediction_data = table_predict.to_dict('records')
    return prediction_data
