from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
# MongoDB Connection
client = MongoClient(


    
)
db = client["ecommerce-db"]
product_collection = db["products"]
order_collection = db["orders"]
customer_collection = db["users"]
print("Database Connected")
app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to E-commerce API"
# GET PRODUCT BY ID
@app.route('/products/<id>', methods=["GET"])
def get_product_by_id(id):
    product = product_collection.find_one({"_id": ObjectId(id)})
    if product:
        product["_id"] = str(product["_id"])
        return jsonify(product)
    return jsonify({"message": "Product not found"})
# GET CUSTOMER BY ID
@app.route('/customers/<id>', methods=["GET"])
def get_customers_by_id(id):
    customer = customer_collection.find_one(
        {"_id": ObjectId(id)}
    )
    if customer:
        customer["_id"] = str(customer["_id"])
        return jsonify(customer)
    return jsonify({"message": "User not found"})
# GET ORDER BY ID
@app.route('/orders/<id>', methods=["GET"])
def get_orders_by_id(id):
    order = order_collection.find_one({"_id": ObjectId(id)})
    if order:
        order["_id"] = str(order["_id"])
        return jsonify(order)
    return jsonify({"message": "Order not found"})
# GET ALL PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    products = []
    product_list = product_collection.find()
    for product in product_list:
        product["_id"] = str(product["_id"])
        products.append(product)
    return jsonify(products)
# GET ALL CUSTOMERS
@app.route('/customers', methods=["GET"])
def get_customers():
    customers = []
    customer_list = customer_collection.find()
    for customer in customer_list:
        customer["_id"] = str(customer["_id"])
        customers.append(customer)
    return jsonify(customers)
# Get All Orders
@app.route('/orders', methods=["GET"])
def get_orders():
    orders = []
    for order in order_collection.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return jsonify(orders)
# ADD PRODUCT
@app.route("/products", methods=['POST'])
def add_product():
    data = request.get_json()
    product = {
        "name": data.get("name"),
        "price": data.get("price"),
        "category": data.get("category"),
        "stock": data.get("stock")
    }
    product_collection.insert_one(product)
    return jsonify({"message": "Product added successfully"})
# ADD CUSTOMER
@app.route('/customers', methods=["POST"])
def add_customer():
    data = request.get_json()
    customer = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone")
    }
    customer_collection.insert_one(customer)
    return jsonify({"message": "Customer added successfully"})
# Add Order
@app.route('/orders', methods=["POST"])
def add_order():
    data = request.get_json()
    order = {
        "customer_name": data.get("customer_name"),
        "product_name": data.get("product_name"),
        "quantity": data.get("quantity"),
        "total_price": data.get("total_price")
    }
    order_collection.insert_one(order)
    return jsonify({
        "message": "Order placed successfully"
    })
# DELETE PRODUCT
@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    product_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted successfully"})
# DELETE CUSTOMER
@app.route("/customers/<id>", methods=["DELETE"])
def delete_customer(id):
    customer_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "coustomer deleted successfully"})
# DELETE ORDER
@app.route("/orders/<id>", methods=["DELETE"])
def delete_order(id):
    order_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "order deleted successfully"})
if __name__ == "__main__":
    app.run(debug=True)
