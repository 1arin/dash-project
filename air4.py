import requests
from pprint import pformat
import pandas as pd

station_id = "44t"
param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"
data_type = "hr"
start_date = "2024-02-19"
end_date = "2024-02-20"
start_time = "00"
end_time = "23"
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()

# Convert the JSON response to a DataFrame
data = pd.DataFrame.from_dict(response_json["stations"][0]["data"])

# Drop columns
data.drop(columns=['PM10', 'CO', 'SO2', 'NO2'], inplace=True)

# Convert 'DATETIMEDATA' to numeric format
data['DATETIMEDATA'] = pd.to_numeric(data['DATETIMEDATA'], errors='coerce')

# Set the threshold for non-null values
threshold_percentage = 50
threshold = len(data) * (1 - threshold_percentage / 100)

# Drop columns with more than 50% NaN values
data.dropna(axis=1, thresh=threshold, inplace=True)

# Fill null values with the mean of each column
data.fillna(data.mean(), inplace=True)

# Replace zeros in specified columns with the mean of each column
columns_to_handle_zeros = ["O3", 'WS']
for column in columns_to_handle_zeros:
    data[column].replace(0, data[column].mean(), inplace=True)

# Convert 'DATETIMEDATA' back to datetime format
data['DATETIMEDATA'] = pd.to_datetime(data['DATETIMEDATA'], unit='s')

print(data)
