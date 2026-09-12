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
# Our ERD structure

┌──────────────┐
│    users     │
├──────────────┤
│ id PK        │
│ name         │
│ email        │
│ password     │
│ phone        │
│ address      │
│ created_at   │
└──────┬───────┘
       │
       │ 1:M
       ▼
┌──────────────┐
│  borrowings  │
├──────────────┤
│ id PK        │
│ user_id FK   │
│ book_id FK   │
│ borrow_date  │
│ due_date     │
│ return_date  │
│ status       │
│ created_at   │
└──────┬───────┘
       │
       │ M:1
       ▼
┌──────────────┐
│    books     │
├──────────────┤
│ id PK        │
│ title        │
│ author       │
│ isbn         │
│ description  │
│ quantity     │
│ available    │
│ category_id  │
│ created_at   │
└──────┬───────┘
       │
       │ M:1
       ▼
┌──────────────┐
│  categories  │
├──────────────┤
│ id PK        │
│ name         │
│ description  │
│ created_at   │
└──────────────┘


┌──────────────┐
│    users     │
└──────┬───────┘
       │ 1:M
       ▼
┌──────────────┐
│  user_roles  │
├──────────────┤
│ user_id PK FK│
│ role_id PK FK│
│ created_at   │
└──────┬───────┘
       │ M:1
       ▼
┌──────────────┐
│    roles     │
├──────────────┤
│ id PK        │
│ name         │
│ description  │
└──────────────┘