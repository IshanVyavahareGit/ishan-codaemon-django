# 🎧 User Audio Management Django App

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/IshanVyavahareGit/ishan-codaemon-django)

This repository contains a full-stack Django application for managing users and their associated audio recordings. It features a RESTful API backend and a simple, interactive dashboard for demonstrating the core functionality.

## Features

- **User Management**: Create, Read, Delete operations for users.
- **Audio Uploads**: Users can upload audio files, with validation for file type and size.
- **Active Audio Logic**: Ensures that only one audio file per user is marked as "active" at any given time.
- **Audio History**: Retains all previous audio uploads as "inactive" for historical purposes.
- **Automatic File Cleanup**: Deleting user or audio records also removes the corresponding files from the media storage, preventing orphan files.
- **Auto-Promotion**: Deleting an active audio file automatically promotes the most recent inactive audio to active status.
- **Interactive Dashboard**: A single-page dashboard built with Django Templates, Bootstrap, and vanilla JavaScript to interact with the API in real-time.
- **Containerized**: Ready to run with Docker and Docker Compose for easy setup.
- **API Testing**: Includes a Postman collection to easily test all available API endpoints.

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: SQLite (for development)
- **Frontend**: Django Templates, Bootstrap 5, Plyr.js, Vanilla JavaScript (Fetch API)
- **Containerization**: Docker, Docker Compose

## Getting Started

You can run this project using either Docker (recommended for ease of use) or a local Python environment.

### 1. Using Docker (Recommended)

This is the simplest way to get the application running.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ishanvyavaharegit/ishan-codaemon-django.git
    cd ishan-codaemon-django
    ```

2.  **Run with Docker Compose:**
    ```sh
    docker-compose up --build
    ```
    This command will build the Docker image, start the container, run database migrations, and start the development server.

3.  **Access the application:**
    -   The dashboard is available at: `http://localhost:8000`
    -   The API is available under the `/api/` prefix.

4.  **(Optional) Seed the database:**
    Open another terminal and run the following command to create a few sample users:
    ```sh
    docker-compose exec web python manage.py seed
    ```

### 2. Local Development Setup

If you prefer to run the application without Docker:

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ishanvyavaharegit/ishan-codaemon-django.git
    cd ishan-codaemon-django/backend
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

5.  **(Optional) Seed the database:**
    Create a few sample users to populate the dashboard.
    ```sh
    python manage.py seed
    ```

6.  **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7.  **Access the application:**
    -   The dashboard is available at: `http://localhost:8000`

## Application Structure

The project is organized into a `backend` Django project, a `postman` directory for API testing, and root-level Docker configuration.

```
.
├── main_app/                 # Contains the Django project
│   ├── backend/              # Django project configuration (settings.py, urls.py)
│   ├── users/                # The main Django app
│   │   ├── migrations/       # Database migrations
│   │   ├── management/       # Custom Django management commands (e.g., 'seed')
│   │   ├── templates/        # Frontend - HTML for the dashboard
│   │   ├── models.py         # AppUser and UserAudio database models
│   │   ├── serializers.py    # DRF serializers for API data conversion
│   │   ├── urls.py           # URL routing for the 'users' app
│   │   └── views.py          # API and template view logic
│   ├── media/                # Directory where uploaded audio files are stored
│   ├── manage.py             # Django's command-line utility
│   └── requirements.txt      # Python dependencies
├── docker-compose.yml        # Docker Compose configuration
├── mp3_samples               # Sample mp3 files to test
└── postman/                  # Postman collection for API testing
```

## API Endpoints

The API is accessible under the `/api/` path.

### User Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/users/` | Lists all users. |
| `POST` | `/api/users/` | Creates a new user. |
| `GET` | `/api/users/<id>/` | Retrieves a single user by their ID. |
| `PUT`/`PATCH`| `/api/users/<id>/` | Updates a user's details. |
| `DELETE` | `/api/users/<id>/` | Deletes a user and all their associated audio files. |

### User Audio Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/users/<id>/audio/` | Retrieves the user's **current active** audio record. |
| `GET` | `/api/users/<id>/audio/?history=1` | Retrieves **all** audio records (active and inactive) for a user. |
| `POST` | `/api/users/<id>/audio/` | Uploads a new audio file. This new file becomes the active one, and any previous active audio is set to inactive. Requires a multipart/form-data request with a `file` field. |
| `DELETE`| `/api/users/<id>/audio/` | Deletes the current active audio record and its associated file. If any inactive audio records remain, the most recent one is automatically promoted to active. |

---

### Testing with Postman

1.  Open Postman.
2.  Go to `File > Import...`.
3.  Select the `postman/Django Backend.postman_collection.json` file from this repository.
4.  The collection will be imported, allowing you to test all API endpoints directly.
