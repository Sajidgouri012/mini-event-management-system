# Event Management API

A mini Event Management System built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL**, following **Clean Architecture** principles.

---

## 📌 Overview

This API allows users to:

- Create events
- Register attendees
- List attendees with pagination
- Filter events by location and date
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

## 📁 Project Structure

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
├── requirements.txt
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_attendees.py
│   └── test_events.py
└── utils
    ├── common.py
    ├── init_db.py
    └── init_db_runner.py

