# Player Stats API

## Project Overview

This project is a comprehensive FastAPI backend designed to support a fictional game. It provides a robust API for managing players, tracking detailed game runs, and calculating player analytics. The application features a secure authentication system for both players and administrators, a well-structured database schema, and a comprehensive test suite to ensure code quality and reliability.

## Key Features

-   **Player Management**: Create new players with securely hashed passwords.
-   **Per-Player Authentication**: Returning players authenticate with their unique password to start new game runs.
-   **Admin Panel Security**: Admin-only endpoints are protected using HTTP Basic Authentication.
-   **Game Run Lifecycle**: Full support for starting, updating (with in-game stats like kills and level), and ending game runs.
-   **Comprehensive Analytics**: Endpoints for detailed player statistics, leaderboards, and other game metrics.
-   **Configuration Management**: Flexible settings management using Pydantic for easy environment configuration.
-   **Automated Testing**: A full suite of tests using `pytest` to ensure API reliability and correctness.

## Tech Stack

-   **Backend Framework**: FastAPI
-   **Database ORM**: SQLAlchemy
-   **Data Validation**: Pydantic
-   **Password Hashing**: Passlib with Bcrypt
-   **Testing**: Pytest, HTTPX
-   **Default Database**: SQLite

## Project Structure

The project is organized into several key modules:

-   `main.py`: The main FastAPI application file containing all API endpoint definitions.
-   `crud.py`: Contains all the functions that interact directly with the database (Create, Read, Update, Delete).
-   `models.py`: Defines the SQLAlchemy database models (e.g., `Player`, `Run`).
-   `schemas.py`: Defines the Pydantic schemas used for data validation and serialization in API requests and responses.
-   `database.py`: Handles the database connection and session management.
-   `config.py`: Manages application settings, such as the database URL.
-   `auth.py`: Contains all authentication logic, including password hashing/verification and admin authentication.
-   `tests/`: Contains all the automated tests for the application.

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.8+
-   An active virtual environment is recommended.

### 2. Clone the Repository

```sh
git clone https://github.com/LucaMcAtarsney/comp-3011-coursework-1.git
cd web-course-work-1
```

### 3. Create and Activate a Virtual Environment

```sh
# Create a virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
.\\venv\\Scripts\\activate
```

### 4. Install Dependencies

Install both the production and development dependencies.

```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

The application is now ready to run. The first time you start the application, it will automatically create a `coursework1.db` SQLite database file.

## Running the Application

To run the development server with live reloading, use `uvicorn`:

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the full suite of automated tests, use `pytest`:

```sh
python -m pytest
```

This command will discover and run all tests in the `tests/` directory, ensuring all parts of the application are working as expected.
