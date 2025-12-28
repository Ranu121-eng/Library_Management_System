-- 1. Create and select the database
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- 2. Table for book inventory
-- Stores details of books available in the library [1]
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    qty INT DEFAULT 0
);

-- 3. Table for library members
-- Uses 'user_name' as the unique identifier for all transactions [1, 2]
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL, -- Unique name chosen during registration
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- Supports secure backend registration
);

-- 4. Table to track book assignments (Lending & Returns)
-- Linked to books and users to ensure data integrity [2, 3]
CREATE TABLE issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    user_name VARCHAR(255), -- References the registered user_name
    issue_date DATE,
    return_date DATE,
    
    -- If a book or user is deleted, their loan records are automatically removed [3]
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (user_name) REFERENCES users(user_name) ON DELETE CASCADE
);

-- 5. Seed data for book inventory
-- Populates your library with initial titles [3, 4]
INSERT INTO books (title, author, genre, qty) VALUES
('The Alchemist', 'Paulo Coelho', 'Fiction', 10),
('To Kill a Mockingbird', 'Harper Lee', 'Classic', 8),
('1984', 'George Orwell', 'Dystopian', 12),
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 7),
('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 15),
('The Catcher in the Rye', 'J.D. Salinger', 'Classic', 5),
('Pride and Prejudice', 'Jane Austen', 'Romance', 9),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 11);

-- 6. Verification queries (Optional)
SELECT * FROM books;
SELECT * FROM users;
SELECT * FROM issued_books;