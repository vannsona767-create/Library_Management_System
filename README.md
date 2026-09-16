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


------------------------------------------------------------------

" Borin work part "

    step 1 :

- write some code on run.py
- write some text on requirements
- write some code on main.py in route folder in app folder
- add init.py to app folder
- write some code on config.py in app folder
- write some code on extensions.py in app folder

goal : python run.py
       	     ↓
	http://127.0.0.1:5000/
             ↓
	Library Management System - Stage 1 setup OK

------------------------------------------------------------------

    step 2 :

I add sql file to our project bcos i need to test user table:

How to import via phpMyAdmin
- Start Apache and MySQL in the XAMPP control panel.
- Open http://localhost/phpmyadmin.
- Click Import in the top menu.
- Choose the file database/library.sql from our project folder.
- Click Go.

------------------------------------------------------------------

    step 3 :

- add some code to __init__.py, book.py, borrowing.py, category.py,
user.py in app/models folder
- add some code to __init__.py in templates folder

goal : for test database working by using cmd