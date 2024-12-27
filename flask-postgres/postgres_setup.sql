-- Switch to or create the 'ecommerce' database
CREATE DATABASE ecommerce;

-- Connect to the 'ecommerce' database
\c ecommerce;

-- Create a new role and grant privileges
CREATE ROLE username WITH LOGIN PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO username;

-- Create the 'products' table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Create the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Grant privileges on tables to the role
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;

-- Grant privileges on sequences to allow auto-increment usage
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO username;

-- Seed some initial data into 'products'
INSERT INTO products (name, price, stock) VALUES
('Sample Product 1', 10.99, 100),
('Sample Product 2', 20.99, 50);

-- Seed an initial user (Note: Replace with hashed passwords in production)
INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', 'password123');
