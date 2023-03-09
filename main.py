from flask import Flask, request, jsonify
import os

app = Flask(__name__)

data = []

def register_user(remote_addr, index=None):
    for dictionary in data:
        if remote_addr in dictionary:
            if index is not None:
                return jsonify(dictionary.get(remote_addr)[index]), 200
            else:
                return jsonify(dictionary.get(remote_addr)), 200
    
    # If remote_addr is not found, create a new dictionary and append it to data
    new_dict = {remote_addr: [
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
        return jsonify(new_dict.get(remote_addr)[index]), 200
    else:
        return jsonify(new_dict.get(remote_addr)), 200


# Get the index of the dictionary that contains the key 'remote_addr'
@app.route('/data')
def get_data():
    remote_addr = request.remote_addr
    for dictionary in data:
        if remote_addr in dictionary:
            return jsonify(dictionary.get(remote_addr))

    # If remote_addr is not found, create a new dictionary and append it to data
    return register_user(remote_addr)

@app.route('/data/<int:index>')
def get_data_index(index):
    remote_addr = request.remote_addr
    for dictionary in data:
        if remote_addr in dictionary:
            if index >= len(dictionary.get(remote_addr)):
                return jsonify('Index out of range, the data you are trying to acess does not exist.'), 400
            return jsonify(dictionary.get(remote_addr)[index])

    
    return register_user(remote_addr, index)

@app.route('/data', methods=['POST'])
def create_data():
    remote_addr = request.remote_addr
    json_data = request.get_json()

    for dictionary in data:
        if remote_addr in dictionary:
            dictionary.get(remote_addr).append(json_data)
            return jsonify(json_data), 200

    if json_data is None:
        return 'Data not provided.', 400

    register_user(remote_addr)

    data[-1][remote_addr].append(json_data)
    return jsonify(json_data), 200


@app.route('/data/<int:index>', methods=['PUT'])
def update_data(index):
    remote_addr = request.remote_addr
    json_data = request.get_json()

    for dictionary in data:
        if remote_addr in dictionary:
            dictionary.get(remote_addr)[index].update(json_data)
            return jsonify(json_data), 200
    
    return 'User not found.', 404

@app.route('/data/<int:index>', methods=['DELETE'])
def delete_data(index):
    remote_addr = request.remote_addr
    for dictionary in data:
        if remote_addr in dictionary:
            if index < len(dictionary.get(remote_addr)):
                del dictionary.get(remote_addr)[index]
                return 'Data deleted successfully.', 200
            else:
                return 'Data index out of range.', 400
    
    return 'Data not found.', 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
