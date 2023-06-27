from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import json


app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.DummyApi
data = []


def register_user(username):
    userCollection = db[username]
    newData = [
        {
            'título': 'Sua História',
            'autor': 'Autora'
        },
        {
            'título': 'Microsoft',
            'autor': 'teste'
        },
        {
            'título': 'do Ano',
            'autor': 'Jeff Bezos'
        }
    ]
    userCollection.insert_many(newData)
    dado = []
    documents = userCollection.find()
    for document in documents:
        # Convert ObjectId to string representation
        document['_id'] = str(document['_id'])
        dado.append(document)
    return jsonify(dado), 200

@app.route('/data/<username>')
def get_data(username):
    if username in db.list_collection_names():
        dado = []
        documents = db[username].find()
        for document in documents:
            # Convert ObjectId to string representation
            document['_id'] = str(document['_id'])
            dado.append(document)
        return jsonify(dado), 200

    # If username is not found, create a new collection and append it to data
    return register_user(username)

@app.route('/data/<username>/<id>')
def get_data_index(username, id):
    try:
        document = db[username].find_one({"_id": ObjectId(id)})
        if document:
            # Convert ObjectId to string representation
            document['_id'] = str(document['_id'])
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except:
        return jsonify({"error": "Id is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"})

@app.route('/data/<username>', methods=['POST'])
def create_data(username):
    json_data = request.get_json()

    if username in db.list_collection_names():
        db[username].insert_one(json_data)
        return jsonify({"message": "Success!"}), 200
    
    register_user()

@app.route('/data/<username>/<id>', methods=['PUT'])
def update_data(username, id):
    json_data = request.get_json()

    if username in db.list_collection_names():
        document = db[username].find_one({"_id": ObjectId(id)})
        
        if document:
            # Update the document with the provided JSON data
            db[username].update_one({'_id': document['_id']}, {'$set': json_data})
            
            # Fetch the updated document
            updated_document = db[username].find_one({'_id': document['_id']})
            
            # Convert ObjectId to string representation
            updated_document['_id'] = str(updated_document['_id'])
            
            return jsonify(updated_document), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/data/<username>/<id>', methods=['DELETE'])
def delete_data(username, id):

    if username in db.list_collection_names():
        db[username].delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Delete succesfull!"})
    
    return 'Data not found.', 404

if __name__ == '__main__':
    app.run(threaded=True,port=os.getenv("PORT", default=5000))