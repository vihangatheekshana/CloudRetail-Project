from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb+srv://Vihanga:Theekviha%4012345@cloudretailcluster.vvnbntb.mongodb.net/?appName=CloudRetailCluster")
db = client["CloudRetail_Final_Assignment"]
orders_collection = db["customer_orders"]

@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    order_id = str(uuid.uuid4())[:8].upper()
    
    order_record = {
        "order_id": order_id,
        "customer_email": data.get('email'),
        "items": data.get('items'),
        "total_amount_lkr": data.get('total_price'),
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "order_status": "Processing"
    }
    orders_collection.insert_one(order_record)
    return jsonify({"message": "Order placed!", "order_id": order_id}), 201

@app.route('/history', methods=['GET'])
def get_history():
    all_orders = list(orders_collection.find({}, {"_id": 0}))
    return jsonify(all_orders)

@app.route('/history', methods=['GET'])
def get_admin_history():
    # Fetch all orders from the customer_orders collection
    all_orders = list(orders_collection.find({}, {"_id": 0}))
    return jsonify(all_orders)

if __name__ == '__main__':
    app.run(port=5003, debug=True)