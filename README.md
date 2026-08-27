# Weather Data Pipeline

A containerized ETL pipeline that extracts multi-city weather forecast data from the Open-Meteo API, validates and transforms the records with Python, and loads them into PostgreSQL for SQL-based analytics.

## Overview

This project demonstrates a complete ETL workflow:

1. Extract weather forecast data from the Open-Meteo API
2. Transform and validate the retrieved records
3. Load valid records into PostgreSQL
4. Prevent duplicate city/date records
5. Analyze stored weather data with SQL
6. Run the application and database together using Docker Compose

The pipeline currently processes weather data for:

- Manisa
- Izmir
- Ankara
- Istanbul
- Bursa

With a 7-day forecast, a standard pipeline run processes 35 weather records.

## Architecture

```text
Open-Meteo API
      |
      v
  extract.py
      |
      v
 transform.py
      |
      v
   load.py
      |
      v
 PostgreSQL
      |
      v
 SQL Analytics
```

Docker Compose runs the application and PostgreSQL as separate containers:

```text
+-------------------+
|   app container   |
|                   |
|   Python ETL      |
+---------+---------+
          |
          | db:5432
          v
+-------------------+
|    db container   |
|                   |
|   PostgreSQL 16   |
+---------+---------+
          |
          v
   postgres_data
      volume
```

## Technologies

- Python 3.13
- PostgreSQL
- SQL
- Open-Meteo API
- psycopg
- requests
- python-dotenv
- uv
- Docker
- Docker Compose
- Git
- GitHub

## Project Structure

```text
weather-data-pipeline/
├── extract.py
├── transform.py
├── load.py
├── main.py
├── sql/
│   ├── init.sql
│   └── analytics.sql
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

## ETL Process

### Extract

`extract.py` sends requests to the Open-Meteo API and retrieves daily forecast data for multiple cities.

The extracted fields include:

- city
- date
- maximum temperature
- minimum temperature
- precipitation

### Transform

`transform.py` validates the extracted weather records before they are loaded into PostgreSQL.

For example, records where the maximum temperature is lower than the minimum temperature are rejected.

### Load

`load.py` connects to PostgreSQL using environment variables and inserts valid weather records into the `weather_data` table.

Duplicate records are prevented using a unique constraint on:

```sql
(city, date)
```

and:

```sql
ON CONFLICT (city, date) DO NOTHING
```

## Database Schema

The PostgreSQL table is initialized automatically with `sql/init.sql`.

```sql
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    max_temp NUMERIC(5,2),
    min_temp NUMERIC(5,2),
    precipitation NUMERIC(6,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(city, date)
);
```

## SQL Analytics

The `sql/analytics.sql` file contains analytical queries using concepts such as:

- filtering and sorting
- aggregate functions
- GROUP BY
- HAVING
- CASE
- subqueries
- ROW_NUMBER
- RANK / DENSE_RANK
- LAG / LEAD
- window functions
- rolling averages
- city-level comparisons

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DB_NAME=weather_db
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

The `.env` file is excluded from Git and the Docker build context.

## Run with Docker

Docker Compose starts both the Python ETL application and PostgreSQL database.

Build and start the services:

```bash
docker compose up --build
```

The application waits until PostgreSQL passes its health check before starting the ETL pipeline.

The database schema is initialized automatically through:

```text
sql/init.sql
```

PostgreSQL data is persisted using a Docker named volume.

Stop the containers:

```bash
docker compose down
```

To completely reset the Docker database and delete its volume:

```bash
docker compose down -v
```

## Verify Stored Data

To check the number of records stored in the Docker PostgreSQL database:

```bash
docker compose exec db psql -U bekir -d weather_db -c "SELECT COUNT(*) FROM weather_data;"
```

For a fresh 5-city, 7-day run, the pipeline normally produces 35 records.

## Run Locally

Install dependencies:

```bash
uv sync
```

Configure the `.env` file with a locally running PostgreSQL instance.

Run the pipeline:

```bash
uv run main.py
```

## Error Handling

The pipeline includes handling for:

- HTTP request failures
- API timeouts
- invalid or missing API data
- missing database configuration
- PostgreSQL connection errors
- pipeline-level failures

Errors are recorded using Python logging and propagated instead of being silently ignored.

## Docker Features

The Docker setup includes:

- Python application image
- PostgreSQL 16 container
- Docker Compose orchestration
- service-to-service networking
- PostgreSQL health checks
- automatic database initialization
- persistent database volume
- environment-based configuration
- Docker build exclusions with `.dockerignore`