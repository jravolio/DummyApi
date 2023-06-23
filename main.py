from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
from bson import json_util

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

@app.route('/data/<username>/<int:id>')
def get_data_index(username, id):
    print(db[username].find({f"_id": f"{id}"}))
    print("teste")
    return jsonify(db[username].find({f"_id": f"{id}"}))

@app.route('/data/<username>', methods=['POST'])
def create_data(username):
    json_data = request.get_json()

    for dictionary in data:
        if username in dictionary:
            dictionary.get(username).append(json_data)
            return jsonify(json_data), 200

    if json_data is None:
        return 'Data not provided.', 400

    register_user(username)

    data[-1][username].append(json_data)
    return jsonify(json_data), 200


@app.route('/data/<username>/<int:index>', methods=['PUT'])
def update_data(username, index):
    json_data = request.get_json()

    for dictionary in data:
        if username in dictionary:
            dictionary.get(username)[index].update(json_data)
            return jsonify(json_data), 200
    
    return 'User not found.', 404

@app.route('/data/<username>/<int:index>', methods=['DELETE'])
def delete_data(username, index):
    for dictionary in data:
        if username in dictionary:
            if index < len(dictionary.get(username)):
                del dictionary.get(username)[index]
                return 'Data deleted successfully.', 200
            else:
                return 'Data index out of range.', 400
    
    return 'Data not found.', 404

if __name__ == '__main__':
    app.run(threaded=True, port=os.getenv("PORT", default=5000))