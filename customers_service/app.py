from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
from mangum import Mangum  # Required for AWS Lambda deployment

app = Flask(__name__)
# Robust CORS setup to allow the frontend to communicate with AWS
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Connection
client = pymongo.MongoClient("mongodb+srv://Vihanga:Theekviha%4012345@cloudretailcluster.vvnbntb.mongodb.net/?appName=CloudRetailCluster")
db = client["CloudRetail_Final_Assignment"]
customers_collection = db["registered_customers"]

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    
    # Check if user already exists
    if customers_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409
    
    user_record = data
    # Ensure role is set for the Admin/Customer logic
    user_record["role"] = data.get("role", "customer") 
    customers_collection.insert_one(user_record)
    return jsonify({"message": "Registration successful!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Validate credentials against MongoDB
    user = customers_collection.find_one({"email": data.get('email'), "password": data.get('password')})
    
    if user:
        return jsonify({
            "message": "Login Successful", 
            "user_name": user.get('full_name', 'User'),
            "role": user.get("role", "customer")
        }), 200
    return jsonify({"error": "Invalid Email or Password"}), 401

# THE MASTER HANDLER: This is what AWS API Gateway calls
handler = Mangum(app)

if __name__ == '__main__':
    # Local testing on Port 5002
    app.run(port=5002, debug=True)