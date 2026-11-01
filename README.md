# Auto Clock-in — Attendance System Backend

A Python backend for a university attendance project. It stores building geofences, timetabled sessions and attendance events, and provides an application programming interface (API) for a mobile client.

The wider project uses a Flutter mobile application to decide when a student is eligible to clock in, handle a five-minute exit grace period and calculate attendance. This repository contains the backend and its browser-based administration pages. The Flutter client is not included in the current repository.

## What this backend does

- Stores buildings with latitude, longitude and geofence radius.
- Stores sessions with start and end times linked to buildings.
- Provides building and session data for client synchronisation.
- Accepts batches of attendance events from the client.
- Returns a session's event history in timestamp order.
- Provides administration pages for buildings, sessions and events.
- Imports session timetables from comma-separated values (CSV) files.

## Technology

| Component | Technology |
| --- | --- |
| API | Python and FastAPI |
| Database | SQLite and SQLAlchemy |
| Validation | Pydantic |
| Administration pages | Jinja2 templates |
| Development server | Uvicorn |

## How it fits together

The mobile client reads building and session data from the API. It then sends attendance events to the backend, which stores them in SQLite. The administration pages let a demonstrator manage buildings, timetables and event records.

The wider project's attendance rules include clocking in within the correct geofence and session time, a five-minute grace period after leaving, and automatic clock-out when a session ends. Those location and timing decisions belong to the mobile client; the backend stores the resulting events.

## Source layout

| Path | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI application and router registration |
| `app/api_routes.py` | Client API routes |
| `app/admin_routes.py` | Administration pages and timetable imports |
| `app/models.py` | Building, session and attendance-event database models |
| `app/schemas.py` | Request and response schemas |
| `app/crud.py` | Database read and write operations |
| `app/database.py` | SQLite connection and database sessions |
| `templates/` | Administration page templates |

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/buildings` | List buildings |
| GET | `/api/sessions` | List sessions |
| GET | `/api/sync/buildings` | Retrieve buildings for synchronisation |
| GET | `/api/sync/sessions` | Retrieve sessions, optionally filtered by date |
| POST | `/api/attendance-events` | Save a batch of attendance events |
| GET | `/api/sessions/{session_id}/events` | Retrieve a session's event history |

The administration pages are available at `/buildings`, `/sessions` and `/events`.

## Local demonstration

The application entry point is `app.main:app`. From the repository root, with the project's dependencies installed in a Python environment, start the development server with:

```bash
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation, or `http://127.0.0.1:8000/buildings` for the buildings page.

The source imports FastAPI, SQLAlchemy, Pydantic, Jinja2 and python-multipart. Uvicorn runs the development server. The current schemas use Pydantic 1-style configuration. A pinned dependency file is not currently included, so a fresh environment has not been verified by this documentation update.

The database path is `sqlite:///./attendance.db`, relative to the working directory. Database tables are created when the application starts.

## Timetable import format

The CSV importer expects these column names:

```csv
title,start_time,end_time,building_id
Example session,2026-11-02T09:00:00,2026-11-02T10:00:00,1
```

Create the corresponding building before importing a session. Dates and times are parsed using Python's ISO-format datetime parser.

## Project scope

Developed as an academic prototype for local demonstration. The current backend has no authentication, and its event endpoint stores client-submitted attendance decisions. A production version would need authentication and server-side attendance validation.

## Author

Virginia Eduwa — MSci Data Science with Applied Business Informatics, Keele University.


This public portfolio copy contains source and templates only. The original local database and private Git history are not included.

