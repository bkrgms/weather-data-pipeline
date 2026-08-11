from extract import get_weather_data
from load import save_weather_data
from transform import validate_weather_data

weather_records = get_weather_data()

valid_records = validate_weather_data(weather_records)

save_weather_data(valid_records)

