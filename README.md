# Group final project
1. Vann Sona -> Leader
2. Kruy Kimty -> member
3. Seven Borinz -> member

# Project Structure
library_management_system/
│
├── run.py                         ← Start Flask
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── database/
│   └── library.sql                ← MySQL database
│
└── app/
    │
    ├── __init__.py                ← Create Flask application
    ├── config.py                  ← Configuration
    │
    ├── extensions.py              ← Database initialization
    │
    ├── models/                    ← Database models
    │   ├── __init__.py
    │   ├── user.py
    │   ├── book.py
    │   ├── category.py
    │   └── borrowing.py
    │
    ├── routes/                    ← Flask routes
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── main.py
    │   ├── books.py
    │   ├── borrowings.py
    │   ├── user.py
    │   └── admin.py
    │
    ├── templates/                 ← Jinja2
    │   │
    │   ├── base.html
    │   ├── home.html
    │   │
    │   ├── auth/
    │   │   ├── login.html
    │   │   └── register.html
    │   │
    │   ├── user/
    │   │   ├── dashboard.html
    │   │   ├── books.html
    │   │   ├── book_detail.html
    │   │   ├── borrowings.html
    │   │   └── profile.html
    │   │
    │   └── admin/
    │       ├── dashboard.html
    │       ├── books.html
    │       ├── add_book.html
    │       ├── edit_book.html
    │       ├── users.html
    │       ├── categories.html
    │       └── borrowings.html
    │
    └── static/
        ├── css/
        │   └── style.css
        │
        ├── js/
        │   └── main.js
        │
        └── images/