from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import os  # Added to read MONGO_URI from AWS Configuration
from mangum import Mangum

app = Flask(__name__)

# Professional CORS setup to allow your Amplify frontend to connect
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Connection using Environment Variable
# Ensure you have 'MONGO_URI' set in your Lambda Configuration tab
MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://Vihanga:Theekviha%4012345@cloudretailcluster.vvnbntb.mongodb.net/?appName=CloudRetailCluster")
client = pymongo.MongoClient(MONGO_URI)
db = client["CloudRetail_Final_Assignment"] 
products_collection = db["assignment_items"] 

@app.route('/products', methods=['GET'])
def get_products():
    try:
        all_products = list(products_collection.find({}, {"_id": 0}))
        return jsonify(all_products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['POST'])
def add_or_update_product():
    new_data = request.json
    name = new_data.get('name')
    if not name:
        return jsonify({"error": "Product name is required"}), 400

    products_collection.update_one({"name": name}, {"$set": new_data}, upsert=True)
    return jsonify({"message": f"Product '{name}' synchronized successfully!"})

@app.route('/products', methods=['DELETE'])
def delete_product_by_name():
    data = request.json
    name = data.get('name') if data else None
    if not name:
        return jsonify({"error": "Product name is required in body"}), 400
        
    result = products_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        return jsonify({"message": f"Product '{name}' deleted successfully!"}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/update-stock', methods=['POST'])
def update_stock():
    data = request.json
    product_name = data.get('product_name')
    quantity_bought = data.get('quantity', 1)
    products_collection.update_one({"name": product_name}, {"$inc": {"stock_quantity": -quantity_bought}})
    return jsonify({"message": "Stock updated!"})

# UPDATED HANDLER NAME: This matches your AWS Handler setting 'app.lambda_handler'
lambda_handler = Mangum(app)

if __name__ == '__main__':
    app.run(port=5001, debug=True)