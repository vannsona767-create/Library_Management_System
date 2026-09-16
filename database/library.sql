-- =====================================================================
-- Library Management System - Database Schema
-- Import this file through phpMyAdmin (or `mysql -u root -p < library.sql`)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS library_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE library_management;

-- ---------------------------------------------------------------------
-- Table: users
-- ---------------------------------------------------------------------
CREATE TABLE users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(120) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: categories
-- ---------------------------------------------------------------------
CREATE TABLE categories (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    description     TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: books
-- ---------------------------------------------------------------------
CREATE TABLE books (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    author              VARCHAR(150) NOT NULL,
    isbn                VARCHAR(20)  NOT NULL UNIQUE,
    category_id         INT,
    description         TEXT,
    published_year      YEAR,
    quantity            INT NOT NULL DEFAULT 1,
    available_quantity  INT NOT NULL DEFAULT 1,
    image               VARCHAR(255),
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_books_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_quantity_nonneg CHECK (quantity >= 0),
    CONSTRAINT chk_available_nonneg CHECK (available_quantity >= 0),
    CONSTRAINT chk_available_le_quantity CHECK (available_quantity <= quantity),

    INDEX idx_books_category (category_id),
    INDEX idx_books_title (title)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table: borrowings
-- ---------------------------------------------------------------------
CREATE TABLE borrowings (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    book_id         INT NOT NULL,
    borrow_date     DATE NOT NULL,
    due_date        DATE NOT NULL,
    return_date     DATE NULL,
    status          ENUM('Borrowed', 'Returned', 'Overdue') NOT NULL DEFAULT 'Borrowed',
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_borrowings_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_borrowings_book
        FOREIGN KEY (book_id) REFERENCES books(id)
        ON DELETE CASCADE,

    INDEX idx_borrowings_user (user_id),
    INDEX idx_borrowings_book (book_id),
    INDEX idx_borrowings_status (status)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Seed data: a few starter categories + one working admin account
-- Default admin login (change the password after first login):
--   email:    admin@library.com
--   password: admin123
-- ---------------------------------------------------------------------
INSERT INTO categories (name, description) VALUES
    ('Fiction', 'Novels and fictional works'),
    ('Non-Fiction', 'Factual and educational books'),
    ('Science', 'Science and technology books'),
    ('History', 'Historical books and biographies');

INSERT INTO users (username, email, password_hash, role) VALUES
    ('admin', 'admin@library.com',
     'scrypt:32768:8:1$7UMlBrJn4tJXD6ou$4b3a87753e38ef27e53e4815570dd3a5ddd86fa9bf72df5fca41dafd15003a66ce7f738788cbf0a17045d2a61b8453e03eed96be2e4638ea9924f7e9a153d716',
     'admin');
