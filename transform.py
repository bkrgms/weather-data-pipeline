def validate_weather_data(weather_records):
    valid_records = []
    
    for record in weather_records:
        max_temp = record["max_temp"]
        min_temp = record["min_temp"]

        if max_temp<min_temp:
            valid_records.append(record)
        
    return valid_records