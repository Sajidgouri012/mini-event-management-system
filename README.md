# Event Management API

A mini Event Management System built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL**, following **Clean Architecture** principles.

---

## 📌 Overview

This API allows users to:

- Create events with unique names
- Register attendees
- List attendees with dynamic pagination
- Filter events by location and date range
- Handle timezones (created in IST, supports dynamic timezone conversion)
- Enforce rate limiting (5 requests/min per IP)
- Prevent overbooking and duplicate registrations

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **FastAPI** (async)
- **SQLAlchemy (async engine)**
- **PostgreSQL** or **SQLite** (for testing)
- **Pydantic** for schema validation
- **SlowAPI** for rate limiting
- **Pytest + HTTPX** for testing
- **Clean architecture + modular separation (CRUD / schemas / routers)**

---

## Requirements

- Python 3.11+
- PostgreSQL

---

## Set Up
- Create .env File
- Add variables and values from sample_env
- Directly want to create database in the tables then run ``` python3 utils/init_db_runner.py ```
- If you want to create tables from SQL queries then check ```schema.sql``` inside ```migration folder```
- run  ``` alembic upgrade head ```

## Install dependencies:
- Create virtual environment
``` python3 -m venv env ```
- install requirements
```
pip install -r requirements.txt
```

## Run locally

``` uvicorn app.main:app --reload ```

## Visit docs

http://127.0.0.1:8000/docs

## Run Tests

``` pytest -v ```

---

## Project Structure

.
├── README.md
├── app
│   ├── __init__.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── attendees.py
│   │   └── events.py
│   ├── database
│   │   ├── __init__.py
│   │   ├── db_connection.py
│   │   └── get_db.py
│   ├── main.py
│   ├── models.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── attendees.py
│   │   └── events.py
│   └── schemas
│       ├── attendees.py
│       └── events.py
├── migrations
│   └── schema.sql
├── requirements.txt
├── sample_env
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_attendees.py
│   └── test_events.py
└── utils
    ├── common.py
    ├── init_db.py
    └── init_db_runner.py

----

## Api Requests

Validations:
- Event **name** must be unique.
- Start time must be before end time.
- Start time must be in the future.

### Create Event
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/events/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "hotel oberoi",
  "location": "near kendriya vidhyalay, gandhi maidan, Ahmedabad",
  "start_time": "2025-07-12T04:53:39.282Z",
  "end_time": "2025-07-14T04:59:39.282Z",
  "max_capacity": 20
}'

### List Event with default timezone filter, timezone can be UTC, Asia/Kolkata etc
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/?tz=UTC' \
  -H 'accept: application/json'

### List Event with default timezone and location filter
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/?location=mumbai&tz=UTC' \
  -H 'accept: application/json'

### List Events with date range filter
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/?start_date=2025-07-15&end_date=2025-07-30' \
  -H 'accept: application/json'

### List Event with all filter
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/?location=mumbai&start_date=2025-07-15&end_date=2025-07-30&tz=UTC' \
  -H 'accept: application/json'

### Register Attendees
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/events/064597ae-354d-4a53-bbe9-29f3918a598f/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "rahil",
  "email": "rahil@gmail.com"
}'

### Get Attendees with pagination
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/064597ae-354d-4a53-bbe9-29f3918a598f/attendees?page=1&page_size=10' \
  -H 'accept: application/json'

### Get Attendees with dynamic/users limit choice pagination
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/events/064597ae-354d-4a53-bbe9-29f3918a598f/attendees?page=1&page_size=1' \
  -H 'accept: application/json'

----