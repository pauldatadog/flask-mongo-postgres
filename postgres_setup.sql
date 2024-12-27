DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'ecommerce') THEN
      CREATE DATABASE ecommerce;
   END IF;
END
$$;

-- Connect to the database
\c ecommerce

-- Create the 'products' table only if it doesn't exist
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Create the 'users' table only if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Grant privileges
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'username') THEN
      CREATE ROLE username WITH LOGIN PASSWORD 'password';
   END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE ecommerce TO username;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO username;

-- Insert initial data if the tables are empty
INSERT INTO products (name, price, stock)
SELECT 'Sample Product 1', 10.99, 100
WHERE NOT EXISTS (SELECT 1 FROM products);

INSERT INTO products (name, price, stock)
SELECT 'Sample Product 2', 20.99, 50
WHERE NOT EXISTS (SELECT 1 FROM products);

INSERT INTO users (username, email, password)
SELECT 'admin', 'admin@example.com', 'password123'
WHERE NOT EXISTS (SELECT 1 FROM users);
