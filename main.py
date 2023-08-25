from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodbdummyapi', 27017)
db = client.DummyApi

def register_user(username):
    userCollection = db[username]
    newData = [
        {
            'title': 'Army Of Stone',
            'author': 'Sawyer Moore'
        },
        {
            'title': 'Gods Of Dusk',
            'author': 'Kennedy Simpson'
        },
        {
            'title': 'Call To The Apocalypse',
            'author': 'Ainsley Moore'
        }
    ]
    userCollection.insert_many(newData)
    data = []
    documents = userCollection.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        data.append(document)
    return jsonify(data), 200

@app.route('/data/<username>')
def get_data(username):
    if username in db.list_collection_names():
        data = []
        documents = db[username].find()
        for document in documents:
            document['_id'] = str(document['_id'])
            data.append(document)
        return jsonify(data), 200

    return register_user(username)

@app.route('/data/<username>/<id>')
def get_data_index(username, id):
    try:
        document = db[username].find_one({"_id": ObjectId(id)})
        if document:
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
        dbResponse = db[username].insert_one(json_data)
        print(dbResponse.inserted_id)
        json_data.update({"_id": str(dbResponse.inserted_id)})
        return jsonify({"message": "Success!", "value":json_data}), 200
    
    register_user()

@app.route('/data/<username>/<id>', methods=['PUT'])
def update_data(username, id):
    json_data = request.get_json()

    if username in db.list_collection_names():
        document = db[username].find_one({"_id": ObjectId(id)})
        
        if document:
            db[username].update_one({'_id': document['_id']}, {'$set': json_data})            
            updated_document = db[username].find_one({'_id': document['_id']})
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
    app.run(threaded=True, host="0.0.0.0" ,port=os.getenv("PORT", default=5003), debug=True)