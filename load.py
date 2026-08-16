import psycopg
import os
import logging 

from dotenv import load_dotenv
load_dotenv()
def save_weather_data(weather_records):  
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not db_name:
        raise ValueError("DB_NAME environment veriable is missing")
    if not db_user:
        raise ValueError("DB_USER environment veriable is missing")
    if not db_host:
        raise ValueError("DB_HOST environment variable is missing")
    if not db_port:
        raise ValueError("DB_PORT environment variable is missing")
    
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            host=db_host,
            port=db_port
        )

    except psycopg.Error as error:
        logging.error("Database connection failed : %s",error)
        raise

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO weather_data
    (city, date, max_temp, min_temp, precipitation)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (city, date) DO NOTHING
    """

    for record in weather_records:
        cursor.execute(
        insert_query,
            (
                record["city"],
                record["date"],
                record["max_temp"],
                record["min_temp"],
                record["precipitation"]
            )
        )

    connection.commit()
    cursor.close()
    connection.close()