
from flask import Flask, request, jsonify, Blueprint
from .db import Database


api_bp = Blueprint('api', __name__)
db = Database()

@api_bp.route('/data/<username>')
def get_data(username):
    if username in db.list_collection_names():
        data = []
        for document in db.documents_in_username(username):
            document['_id'] = str(document['_id'])
            data.append(document)
        return jsonify(data), 200

    return jsonify(db.register_user(username=username)), 200

@api_bp.route('/data/<username>/<id>')
def get_data_index(username, id):
    try:
        document = db.find_one_id(username, id)
        if document:
            document['_id'] = str(document['_id'])
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except:
        return jsonify({"error": "Id is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"})

@api_bp.route('/data/<username>', methods=['POST'])
def create_data(username):
    json_data = request.get_json()
    if username in db.list_collection_names():
        json_data.update({"_id": str(db.insert_one(username, json_data).inserted_id)})
        return jsonify({"message": "Success!", "value":json_data}), 200
    
    return jsonify(db.register_user(username), 200)

@api_bp.route('/data/<username>/<id>', methods=['PUT'])
def update_data(username, id):
    json_data = request.get_json()

    if username in db.list_collection_names():
        document = db.find_one_id(username, id)
        
        if document:
            db.update_one(username, json_data, id)            
            updated_document = db.find_one_id(username, id)
            updated_document['_id'] = str(updated_document['_id'])
            
            return jsonify(updated_document), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    else:
        return jsonify({"error": "User not found"}), 404


@api_bp.route('/data/<username>/<id>', methods=['DELETE'])
def delete_data(username, id):
    if username in db.list_collection_names():
        db.delete_one(username, id)
        return jsonify({"message": "Delete succesfull!"})
    
    return 'Data not found.', 404
