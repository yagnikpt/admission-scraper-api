# Admissions API

A RESTful API for accessing admission announcements and related programs from educational institutions. This API provides a way to retrieve announcements with their associated institution, state, and program data.

## Project Overview

This API serves data from a PostgreSQL database containing educational institutions' admission announcements. It allows clients to:

- Retrieve all announcements with their related data
- Fetch specific announcements by ID
- Get a random selection of admission dates announcements

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapper (ORM)
- **Pydantic**: Data validation and settings management
- **PostgreSQL**: Database for storing announcement data

## Project Structure

```
sgh-api/
├── app/                    # Main application package
│   ├── api/                # API routes
│   │   ├── endpoints/      # API endpoint modules
│   │   │   └── announcements.py  # Announcement endpoint handlers
│   │   └── api.py          # Main API router
│   ├── db/                 # Database modules
│   │   ├── models.py       # SQLAlchemy ORM models
│   │   └── session.py      # Database connection handling
│   ├── schemas/            # Pydantic models (schemas)
│   │   ├── announcement.py # Announcement schemas
│   │   ├── institution.py  # Institution schemas
│   │   └── program.py      # Program schemas
│   └── main.py             # Application factory
├── main.py                 # Entry point
└── requirements.txt        # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sgh-api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   DB_URL=postgresql://username:password@localhost:5432/dbname
   ```
   Replace with your PostgreSQL connection details.

## Running the Application

Start the API server:
```
uvicorn app.main:app --reload
```

The server will run at `http://localhost:8000` by default.

## API Endpoints

### Get All Announcements
```
GET /api/announcements
```
Returns all announcements with their related programs, institution, and state information.

### Get Admission Dates Announcements
```
GET /api/announcements/admission-dates
```
Returns up to 10 random announcements with `announcement_type="admission_dates"` and their related data.

### Get Specific Announcement
```
GET /api/announcements/{announcement_id}
```
Returns a specific announcement by ID with all related data.

## Data Models

### Announcement
- `announcement_id`: UUID
- `title`: String
- `content`: String
- `url`: String
- `institution_id`: UUID (optional)
- `state_id`: UUID (optional)
- `published_date`: Date (optional)
- `application_open_date`: Date (optional)
- `application_deadline`: Date (optional)
- `term`: String (optional)
- `contact_info`: String (optional)
- `announcement_type`: String (optional)
- `programs`: Array of Program objects
- `institution`: Institution object (optional)
- `state`: State object (optional)

### Program
- `program_id`: UUID
- `name`: String
- `description`: String (optional)
- `degree_level`: String (optional)
- `duration_months`: Integer (optional)

### Institution
- `institution_id`: UUID
- `name`: String
- `website`: String
- `description`: String (optional)
- `state_id`: UUID (optional)
- `state`: State object (optional)

### State
- `state_id`: UUID
- `name`: String
- `abbreviation`: String

## Documentation

Interactive API documentation is available when the application is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

To add new features or modify existing ones:

1. Add or modify SQLAlchemy models in `app/db/models.py`
2. Create or update Pydantic schemas in the `app/schemas/` directory
3. Implement new API endpoints in `app/api/endpoints/`
4. Register new routers in `app/api/api.py`