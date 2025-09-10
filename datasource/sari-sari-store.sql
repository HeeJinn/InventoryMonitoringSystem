-- Sari-Sari Store Inventory System
-- Create Database
CREATE DATABASE IF NOT EXISTS sari_sari_store;
USE sari_sari_store;

-- Customer Table
CREATE TABLE IF NOT EXISTS customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    contact_number VARCHAR(15),
    address VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items Table
CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions Table (with date_added)
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    item_id INT,
    quantity INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_added DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- Insert Customers (10 customers)
INSERT INTO customer (first_name, last_name, contact_number, address) VALUES
('Juan', 'Dela Cruz', '09171234567', 'Barangay Uno'),
('Maria', 'Santos', '09281234567', 'Barangay Dos'),
('Jose', 'Reyes', '09351234567', 'Barangay Tres'),
('Ana', 'Lopez', '09451234567', 'Barangay Uno'),
('Mark', 'Villanueva', '09561234567', 'Barangay Cuatro'),
('Grace', 'Cruz', '09671234567', 'Barangay Dos'),
('Pedro', 'Marquez', '09781234567', 'Barangay Tres'),
('Liza', 'Ramos', '09891234567', 'Barangay Uno'),
('Carlos', 'Garcia', '09991234567', 'Barangay Cuatro'),
('Elena', 'Torres', '09181234567', 'Barangay Dos');

-- Insert Items (10 items)
INSERT INTO items (item_name, category, price, stock_quantity) VALUES
('Softdrinks 1L', 'Beverages', 45.00, 50),
('Instant Noodles', 'Food', 15.00, 100),
('Laundry Soap', 'Household', 10.00, 200),
('Canned Sardines', 'Food', 25.00, 80),
('Coffee Sachet', 'Beverages', 7.00, 150),
('Biscuits', 'Snacks', 12.00, 90),
('Cooking Oil 500ml', 'Household', 65.00, 40),
('Shampoo Sachet', 'Personal Care', 6.00, 120),
('Toothpaste Small', 'Personal Care', 20.00, 60),
('Rice per Kilo', 'Food', 40.00, 200);

-- Insert Transactions (40 transactions)
INSERT INTO transactions (customer_id, item_id, quantity, total_amount, date_added) VALUES
-- Original 20
(1, 1, 2, 90.00, '2025-08-01'),
(2, 2, 5, 75.00, '2025-08-01'),
(3, 4, 3, 75.00, '2025-08-02'),
(4, 3, 10, 100.00, '2025-08-02'),
(5, 5, 8, 56.00, '2025-08-03'),
(6, 6, 4, 48.00, '2025-08-03'),
(7, 7, 1, 65.00, '2025-08-04'),
(8, 8, 10, 60.00, '2025-08-04'),
(9, 9, 2, 40.00, '2025-08-05'),
(10, 10, 5, 200.00, '2025-08-05'),
(1, 2, 3, 45.00, '2025-08-06'),
(2, 6, 6, 72.00, '2025-08-06'),
(3, 1, 1, 45.00, '2025-08-07'),
(4, 5, 12, 84.00, '2025-08-07'),
(5, 7, 2, 130.00, '2025-08-08'),
(6, 9, 3, 60.00, '2025-08-08'),
(7, 10, 4, 160.00, '2025-08-09'),
(8, 3, 15, 150.00, '2025-08-09'),
(9, 4, 6, 150.00, '2025-08-10'),
(10, 8, 20, 120.00, '2025-08-10'),


(1, 5, 15, 105.00, '2025-08-11'),
(2, 9, 1, 20.00, '2025-08-11'),
(3, 7, 2, 130.00, '2025-08-12'),
(4, 2, 7, 105.00, '2025-08-12'),
(5, 3, 20, 200.00, '2025-08-13'),
(6, 1, 4, 180.00, '2025-08-13'),
(7, 6, 10, 120.00, '2025-08-14'),
(8, 10, 8, 320.00, '2025-08-14'),
(9, 8, 5, 30.00, '2025-08-15'),
(10, 4, 12, 300.00, '2025-08-15'),
(1, 9, 4, 80.00, '2025-08-16'),
(2, 7, 3, 195.00, '2025-08-16'),
(3, 5, 20, 140.00, '2025-08-17'),
(4, 6, 8, 96.00, '2025-08-17'),
(5, 8, 12, 72.00, '2025-08-18'),
(6, 2, 10, 150.00, '2025-08-18'),
(7, 1, 6, 270.00, '2025-08-19'),
(8, 3, 25, 250.00, '2025-08-19'),
(9, 10, 2, 80.00, '2025-08-20'),
(10, 6, 15, 180.00, '2025-08-20');
