### IMPORTS ###
from flask import Flask, jsonify, abort
from flask_cors import CORS

import handlers.data_handler as data_handler
######

### SETUP ###
app = Flask(__name__)
CORS(app, origins=['http://localhost:4200', 'http://localhost:4200/*'])
######

### ROUTES ###
# GET
@app.route('/', methods=['GET'])
def base_route():
    return jsonify('Mateo Sakoman - 1865383')

@app.route('/data/record', methods=['GET'])
def get_records():
    return jsonify(data_handler.get_records())

@app.route('/data/model', methods=['GET'])
def get_models():
    return jsonify(data_handler.get_models())

@app.route('/data/record/<file_name>/<id>/lime', methods=['GET'])
def get_lime(file_name, id):
    return jsonify("Get LIME values for: " + file_name + "/" + id)

# POST
@app.route('/data/record', methods=['POST'])
def upload_record():
    return jsonify("Upload Record")

@app.route('/data/model', methods=['POST'])
def upload_model():
    return jsonify("Upload Model")

@app.route('/data/user-info/connection', methods=['POST'])
def upload_user_info_connection():
    return jsonify("Upload Connection")

@app.route('/data/user-info/evaluation/<file_name>', methods=['POST'])
def upload_user_info_evaluation(file_name):
    return jsonify("Upload Evaluation for " + file_name)

# DELETE
@app.route('/data/record/<file_name>', methods=['DELETE'])
def delete_record(file_name):
    response = data_handler.delete_file('BE/data/record', file_name)
    if response.success == False:
        abort(response.error_code, response.message)
    return jsonify(response.__dict__), response.error_code

@app.route('/data/model/<file_name>', methods=['DELETE'])
def delete_model(file_name):
    response = data_handler.delete_file('BE/data/model', file_name)
    if response.success == False:
        abort(response.error_code, response.message)
    return jsonify(response.__dict__), response.error_code
######

if __name__ == '__main__':
    app.run(debug=True)