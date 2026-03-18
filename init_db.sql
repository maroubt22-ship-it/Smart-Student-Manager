-- ============================================
-- Smart Student Manager - MySQL Database Init
-- SQL script to create database and tables
-- ============================================

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS smart_student_db;

-- Use the database
USE smart_student_db;

-- ============================================
-- Create Students Table
-- Stores all student information
-- ============================================
CREATE TABLE IF NOT EXISTS students (
    -- Primary key: auto-incrementing unique identifier
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    -- Student name: max 100 characters
    name VARCHAR(100) NOT NULL,
    
    -- Age in years: integer value
    age INT NOT NULL,
    
    -- Field of study: max 100 characters
    field_of_study VARCHAR(100) NOT NULL,
    
    -- Timestamp when record was created
    -- Automatically set to current timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index on created_at for faster queries
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Verify table creation
-- ============================================
-- Show table structure (for debugging)
-- DESCRIBE students;

-- ============================================
-- Insert sample data (optional)
-- Uncomment to add test data
-- ============================================
/*
INSERT INTO students (name, age, field_of_study) VALUES
('Ahmed Mohamed', 20, 'Computer Science'),
('Fatima Ali', 19, 'Business Administration'),
('Hassan Ibrahim', 21, 'Civil Engineering'),
('Layla Hassan', 20, 'Medicine'),
('Muhammad Karim', 22, 'Physics');
*/

-- Show results
SELECT 'Database and tables created successfully!' AS status;
