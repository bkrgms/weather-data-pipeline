create table if not exists weather_data(
    id serial primary key,
    city varchar(50) not null,
    date date not null,
    max_temp numeric (5,2),
    min_temp numeric (5,2),
    precipitation numeric (6,2),
    created_at timestamp default current_timestamp,
    unique(city,date)
);