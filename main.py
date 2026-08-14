import logging

from extract import get_weather_data
from load import save_weather_data
from transform import validate_weather_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Pipeline started.")


weather_records = get_weather_data()
logging.info("Extract completed. %s records",len(weather_records))

valid_records = validate_weather_data(weather_records)
logging.info("Transform completed. %s valid records",len(weather_records))

save_weather_data(valid_records)
logging.info("Load completed. %s Load completed",len(weather_records))

logging.info("Pipeline completed.")

