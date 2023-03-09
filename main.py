from flask import Flask, request, jsonify
import os

app = Flask(__name__)

data = []

def register_user(username, index=None):
    for dictionary in data:
        if username in dictionary:
            if index is not None:
                return jsonify(dictionary.get(username)[index]), 200
            else:
                return jsonify(dictionary.get(username)), 200
    
    # If username is not found, create a new dictionary and append it to data
    new_dict = {username: [
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
    ]}
    data.append(new_dict)

    if index is not None:
        return jsonify(new_dict.get(username)[index]), 200
    else:
        return jsonify(new_dict.get(username)), 200


# Get the index of the dictionary that contains the key 'username'
@app.route('/data')
def get_data(username):
    for dictionary in data:
        if username in dictionary:
            return jsonify(dictionary.get(username))

    # If username is not found, create a new dictionary and append it to data
    return register_user(username)

@app.route('/data/<int:index>')
def get_data_index(username, index):
    username = request.username
    for dictionary in data:
        if username in dictionary:
            if index >= len(dictionary.get(username)):
                return jsonify('Index out of range, the data you are trying to acess does not exist.'), 400
            return jsonify(dictionary.get(username)[index])

    
    return register_user(username, index)

@app.route('/data', methods=['POST'])
def create_data(username):
    username = request.username
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


@app.route('/data/<int:index>', methods=['PUT'])
def update_data(username, index):
    username = request.username
    json_data = request.get_json()

    for dictionary in data:
        if username in dictionary:
            dictionary.get(username)[index].update(json_data)
            return jsonify(json_data), 200
    
    return 'User not found.', 404

@app.route('/data/<int:index>', methods=['DELETE'])
def delete_data(username, index):
    username = request.username
    for dictionary in data:
        if username in dictionary:
            if index < len(dictionary.get(username)):
                del dictionary.get(username)[index]
                return 'Data deleted successfully.', 200
            else:
                return 'Data index out of range.', 400
    
    return 'Data not found.', 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
