# 🎧 User Audio Management App

A small full-stack Django application that manages **users** and their **audio recordings**.

Features:

- User CRUD (create, list, update, delete)
- Upload / replace audio per user
- Exactly one **active** audio per user at a time
- Full audio history retained (active + inactive)
- File cleanup on delete (no orphan media files)
- Simple dashboard UI (Django template + Bootstrap) to demonstrate the flow end-to-end
- Postman collection for easy API inspection

---

## 1. Tech Stack

**Backend**

- Python 3.10+
- Django
- Django REST Framework
- SQLite (default dev DB)

**Frontend**

- Django templates
- Bootstrap 5 (CDN)
- Vanilla JavaScript (`fetch` API)

**Storage**

- DB: `db.sqlite3` (users + audio metadata)
- Files: `media/user_audio/` (actual audio files)

---

## 2. Project Structure
`
repo-root/
│
├── backend/
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   │
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── users/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── users/
│   │   │       └── dashboard.html      # main UI
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── media/
│       └── user_audio/                 # uploaded audio files
│
│
│
├── postman/
│   └── user-audio-api-collection.json  # exported Postman collection for api testing
│
└── README.md
`
