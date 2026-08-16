import requests
import logging

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    weather_records = [] #list
    cities= [
        {
            "name":"Manisa",
            "latitude":38.61,
            "longitude":27.43,
        },
        {
            "name":"Izmir",
            "latitude":38.42,
            "longitude":27.14,
        },
        {
            "name":"Ankara",
            "latitude":39.93,
            "longitude":32.86,
        },
        {
            "name":"Istanbul",
            "latitude":41.01,
            "longitude":28.97,
        },
        {
            "name":"Bursa",
            "latitude":40.20,
            "longitude":29.06,
        }
    ]
    for city in cities:
        params = { # dictionary
        "latitude":city["latitude"],
        "longitude":city["longitude"],
        "daily":"temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone":"Europe/Istanbul"
    }
        try:
            response = requests.get(url,params=params,timeout=10)
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            logging.error("Weather API requests failed: %s",error)
            raise    

        daily_data = data.get("daily")
        if not daily_data:
            raise ValueError("Weather API response does not contain daily data")
        dates = daily_data["time"]
        max_temps = daily_data["temperature_2m_max"]
        min_temps = daily_data["temperature_2m_min"]
        precipitations = daily_data["precipitation_sum"]

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
                "precipitation":precipitation,
                "city":city["name"]
            }
            weather_records.append(weather_record)
    if not weather_records:
        raise ValueError("Weather API returned no weather records")
    return weather_records