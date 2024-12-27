import os
from flask import Flask, request, jsonify
import psycopg

# Initialize Flask app

POSTGRES_URI = os.getenv('POSTGRES_URI', 'postgresql://username:password@localhost:5432/ecommerce')

app = Flask(__name__)

# PostgreSQL configuration
# DB_CONFIG = {
#     "dbname": "ecommerce",
#     "user": "username",
#     "password": "password",
#     "host": "localhost",
#     "port": "5432"
# }

# # Helper function to get a database connection
# def get_db_connection():
#     return psycopg.connect(**DB_CONFIG)

# Function to get a database connection
def get_db_connection():
    return psycopg.connect(POSTGRES_URI)

# API to add a product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    if not data or not all(k in data for k in ("name", "price", "stock")):
        return jsonify({"error": "Missing required fields"}), 400

    query = """
    INSERT INTO products (name, price, stock)
    VALUES (%s, %s, %s)
    RETURNING id
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query, (data["name"], data["price"], data["stock"]))
        product_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added", "id": product_id}), 201

# API to list all products
@app.route('/products', methods=['GET'])
def list_products():
    query = "SELECT id, name, price, stock FROM products"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        products = cur.fetchall()
    conn.close()

    result = [{"id": row[0], "name": row[1], "price": row[2], "stock": row[3]} for row in products]
    return jsonify(result), 200

# API to get product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    query = "SELECT id, name, price, stock FROM products WHERE id = %s"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query, (product_id,))
        product = cur.fetchone()
    conn.close()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    result = {"id": product[0], "name": product[1], "price": product[2], "stock": product[3]}
    return jsonify(result), 200

# API to update product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)
    values.append(product_id)

    query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query, tuple(values))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated"}), 200

# API to delete product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    query = "DELETE FROM products WHERE id = %s"
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query, (product_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted"}), 200

# API to register a user
@app.route('/users', methods=['POST'])
def register_user():
    data = request.json
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    query_check = "SELECT 1 FROM users WHERE email = %s OR username = %s"
    query_insert = """
    INSERT INTO users (username, email, password)
    VALUES (%s, %s, %s)
    RETURNING id
    """
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(query_check, (data["email"], data["username"]))
        if cur.fetchone():
            conn.close()
            return jsonify({"error": "User already exists"}), 400

        cur.execute(query_insert, (data["username"], data["email"], data["password"]))
        user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered", "id": user_id}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
