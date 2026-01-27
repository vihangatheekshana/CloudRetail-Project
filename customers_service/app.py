from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient("mongodb+srv://Vihanga:Theekviha%4012345@cloudretailcluster.vvnbntb.mongodb.net/?appName=CloudRetailCluster")
db = client["CloudRetail_Final_Assignment"]
customers_collection = db["registered_customers"]

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    if customers_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409
    
    user_record = data
    user_record["role"] = "customer" # Default role
    customers_collection.insert_one(user_record)
    return jsonify({"message": "Registration successful!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = customers_collection.find_one({"email": data.get('email'), "password": data.get('password')})
    if user:
        return jsonify({
            "message": "Login Successful", 
            "user_name": user['full_name'],
            "role": user.get("role", "customer")
        }), 200
    return jsonify({"error": "Invalid Email or Password"}), 401

if __name__ == '__main__':
    app.run(port=5002, debug=True)