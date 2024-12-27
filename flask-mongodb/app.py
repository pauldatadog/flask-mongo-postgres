import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize Flask app
app = Flask(__name__)

# MongoDB client setup
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ecommerce')
client = MongoClient(mongo_uri)
db = client["ecommerce"]

# Initialize collections and seed data if necessary
def initialize_database():
    # Check if 'products' collection exists
    if 'products' not in db.list_collection_names():
        print("Initializing database...")
        # Create collections
        db.create_collection('products')
        db.create_collection('users')

        # Seed initial data
        db['products'].insert_many([
            { "name": "Sample Product 1", "price": 10.99, "stock": 100 },
            { "name": "Sample Product 2", "price": 20.99, "stock": 50 }
        ])
        db['users'].insert_one({
            "username": "admin",
            "email": "admin@example.com",
            "password": "password123"  # Avoid plain-text passwords in production
        })
        print("Database initialized.")

# Call the initialization function
initialize_database()

products_collection = db["products"]
users_collection = db["users"]

# API to add a product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if not data or not all(k in data for k in ("name", "price", "stock")):
        return jsonify({"error": "Missing required fields"}), 400

    product = {
        "name": data["name"],
        "price": data["price"],
        "stock": data["stock"]
    }
    result = products_collection.insert_one(product)
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

# API to list all products
@app.route('/products', methods=['GET'])
def list_products():
    products = list(products_collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products), 200

# API to get product by ID
@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            return jsonify({"error": "Product not found"}), 404
        product["_id"] = str(product["_id"])
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": "Invalid product ID"}), 400

# API to update product
@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    try:
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product updated"}), 200
    except Exception as e:
        return jsonify({"error": "Invalid product ID"}), 400

# API to delete product
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product deleted"}), 200
    except Exception as e:
        return jsonify({"error": "Invalid product ID"}), 400

# API to register a user
@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "username": data["username"],
        "email": data["email"],
        "password": data["password"]  # Note: Never store passwords as plain text in production
    }
    result = users_collection.insert_one(user)
    return jsonify({"message": "User registered", "id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
