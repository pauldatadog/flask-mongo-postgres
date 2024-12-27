db = db.getSiblingDB('ecommerce'); // Switch to 'ecommerce' database or create it

// Create collections
db.createCollection('products');
db.createCollection('users');

// Optional: Insert some seed data
db.products.insertMany([
    { name: 'Beautiful Sweater', price: 10.99, stock: 100 },
    { name: 'Stylish Jacket', price: 20.99, stock: 50 }
]);

db.users.insertOne({
    username: 'admin',
    email: 'admin@example.com',
    password: 'password123' // Avoid storing plain text passwords in production
});
