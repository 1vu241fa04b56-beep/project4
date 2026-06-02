from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson.objectid import ObjectId
#users = []
client=MongoClient('mongodb+srv://vu241fa04b56:241fa04b56@cluster0.vr7q3nm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db=client["Users-CRT"]
user_collection=db["users"]
print('DB CONNECTED')
app=Flask(__name__)
@app.route('/')
def home():
    return "Hello Welcome to FLASK"
@app.route('/users', methods=['GET'])
def get_users():
    users=[]
    user_list=user_collection.find()
    for user in user_list:
        user["_id"]=str(user["_id"])
        users.append(user)
    return jsonify(users)
@app.route('/users', methods=['POST'])
def add_user():
    data=request.get_json()
    user= {
        "name":data.get("name"),
        "email":data.get("email")
    }
    user_collection.insert_one(user)
    return "Users Inserted Succesfully"
    return jsonify(data)
@app.route('/users/<id>', methods=['GET'])
def get_user_byID(id):
    user=user_collection.find_one(ObjectId(id))
    if user:
        user["_id"]=str(user["_id"])
    return jsonify(user)    
    # return jsonify({"message": "User not found"})
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user_collection.delete_one({"_id":ObjectId(id)})
    return jsonify({"message":"user deleted successfully"})
    #return jsonify({"message": "User not found"})
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    updated_data={
        "name":data.get("name"),
        "email":data.get("email")
    }
    user_collection.update_one({"_id":ObjectId(id)},
    {"$set":updated_data})
    return jsonify({"message": "User updated successfully"})
    #return jsonify({"message": "User not found"})
@app.errorhandler(404)
def unavailable_page(error):
    return jsonify({"message":"Sorry page not available,please go away"})
if __name__=="__main__":
    app.run(debug=True)