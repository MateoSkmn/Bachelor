### IMPORTS ###
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

import handlers.data_handler as data_handler
import handlers.file_handler as file_handler
import handlers.csv_editor_handler as csv_editor
import handlers.lime_handler as lime_handler
######

### SETUP ###
app = Flask(__name__)
CORS(app, origins=['http://localhost:4200', 'http://localhost:4200/*'])
#TODO: Check for '' and ""
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
    return lime_handler.explanation(file_name, id)

# POST
@app.route('/data/record', methods=['POST'])
def upload_record():
    response = file_handler.upload_file(app, "../data/record")
    if response.success == False:
        abort(response.code, response.message)
    return jsonify(response.__dict__), response.code

@app.route('/data/model', methods=['POST'])
def upload_model():
    response = file_handler.upload_file(app, "../data/model")
    if response.success == False:
        abort(response.code, response.message)
    return jsonify(response.__dict__), response.code

@app.route('/data/user-info/connection', methods=['POST'])
def upload_user_info_connection():
    data = request.json
    csv_editor.add_csv_line("BE/Data/UserInfo/connections.csv", data)
    #TODO: Überdenken!!
    return jsonify("Upload Connection")

@app.route('/data/user-info/evaluation/<file_name>', methods=['POST'])
def upload_user_info_evaluation(file_name):
    data = request.json
    path = "BE/Data/UserInfo/Evaluation/" + file_name + ".csv"
    response = csv_editor.add_csv_line(path, data)

    if response.success == True:
        return jsonify(response.__dict__)
    abort(response.code, response.message)

# DELETE
@app.route('/data/record/<file_name>', methods=['DELETE'])
def delete_record(file_name):
    response = file_handler.delete_file('BE/data/record', file_name)
    if response.success == False:
        abort(response.code, response.message)
    return jsonify(response.__dict__), response.code

@app.route('/data/model/<file_name>', methods=['DELETE'])
def delete_model(file_name):
    response = file_handler.delete_file('BE/data/model', file_name)
    if response.success == False:
        abort(response.code, response.message)
    return jsonify(response.__dict__), response.code
######

if __name__ == '__main__':
    app.run(debug=True)