import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude":38.61,
    "longitude":27.43,
    "daily":"temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone":"Europe/Istanbul"
}
response = requests.get(url,params=params)
data = response.json()

daily_data = data["daily"]

dates = daily_data["time"]
max_temps = daily_data["temperature_2m_max"]
min_temps = daily_data["temperature_2m_min"]
precipitations = daily_data["precipitation_sum"]

weather_records = []
for date,max_temp, min_temp, precipitation in zip(
    dates,
    max_temps,
    min_temps,
    precipitations
):
    weather_record = {
        "date":date,
        "max_temp":max_temp,
        "min_temp":min_temp,
        "precipitation":precipitation
    }
    weather_records.append(weather_record)
print(weather_records)

