# Opusmatch

This is a project template which uses FastAPI, Alembic and async SQLModel as ORM.


## Tech Stacks
* FastAPI
* SQLAlchemy 2.0 Models and ORM using AsyncSession and Async DB Statements
* Alembic with automatic Models Migration
* Pydantic with custom validation and Settings
* CORS
* Uvicorn and Gunicorn for Python web server

## Folder Structure
```Bash
├── .env # Contains environment variables for the function
├── app # Main logic code
│   ├── apis # The views layer
│   │   ├── __init__.py
│   │   ├── applicant.py # The applicant endpoint
│   │   ├── job.py # The job endpoint
│   │   └── worker.py # The worker endpoint
│   ├── controllers # The controllers layer
│   │   ├── __init__.py
│   │   ├── applicant.py # The applicant controller
│   │   ├── job.py # The job controller
│   │   └── worker.py # The worker controller
│   ├── database # The models layer
│   │   ├── __init__.py
│   │   ├── config.py # Config naming convention for database
│   │   ├── depends.py # Add dependency for database
│   │   └── models.py # Declare models
│   ├── exceptions # Exception for app
│   │    ├── __init__.py
│   │    ├── configure_logging.py # Config for logging
│   │    └── handle_exception.py # Executes when an exception is thrown. 
│   ├── schemas # Schemas for response models
│   │   ├── __init__.py
│   │   ├── applicant.py # The applicant schema
│   │   ├── job.py # The job schema
│   │   └── worker.py # The worker schema
│   ├── utils #  Utility for app
│   │   ├── __init__.py
│   │   └── common.py # The common functions using for app
│   ├── __init__.py
│   ├── _version.py
│   ├── config.py # Config for main app (paging, database, app)
│   ├── configure_logging.py # Some reasonable defaults and handle those settings
│   └──main.py # Init app, declare route, swagger
├── migrations # Migrations database version
├── README.md
├── requirements.in
└── requirements.txt
```

## Set environment variables
Create an .env file on root folder and copy the content from .env.example. Feel free to change it according to your own configuration.
```
cp .env.example .env
```

## Run the project using Docker containers
```
docker-compose up -d --build   
```


## Run the project without Docker
### Requirements
- **Python 3.8.10**
- **PostgreSQL** v12.x, create user and database to use using your favorite tools, (pdAdmin, DBeaver, Command, etc)


### Installation
```
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```


### Migrations
```
# Fixed model changes
alembic revision --autogenerate -m "<revision name>"

# Apply changes to database
alembic upgrade head
```

### Run app
```
uvicorn main:app --reload
```


## API Documentation  (provided by Swagger UI)
After running, you can access the documentation (Swagger) with the following path http://localhost:8080/api/v1


## Screenshots
![Screenshots](https://github.com/nnpvaan/opusmatch_challenge/blob/develop/templates/img.png)