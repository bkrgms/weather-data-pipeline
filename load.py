import psycopg

def save_weather_data(weather_records):
    connection = psycopg.connect(
    dbname="weather_db",
    user="bekir",
    host="localhost",
    port="5432"
)

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