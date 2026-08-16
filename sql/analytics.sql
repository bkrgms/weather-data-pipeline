/* Weather statistics by city */
select
    city,
    count(*) as record_count,
    avg(max_temp) as average_max_temp,
    max(max_temp) as highest_temp,
    min(min_temp) as lowest_temp
from weather_data
group by city
order by average_max_temp desc;

/* 3-day rolling average by city */
select
    city,
    date,
    max_temp,
    avg(max_temp) over (
        partition by city
        order by date
        rows between 2 preceding and current row
    ) as rolling_3_day_avg
from weather_data
order by city,date

/* Hottest day of each city compared with city average*/
select 
    city,
    date,
    max_temp,
    city_temp_avg,
    max_temp - city_temp_avg as difference_from_average
from(
    select
        city,
        date,
        max_temp,

        row_number() over(
            partition by city
            order by max_temp desc
        ) as rn,

        avg(max_temp) over(
            partition by city
        ) as city_temp_avg

        from weather_data
) as city_weather_analysis
where rn = 1
order by max_temp desc;