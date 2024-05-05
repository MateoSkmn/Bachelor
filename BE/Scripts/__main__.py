### IMPORTS ###
import os
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

# Check if the connections.csv file exists
if not os.path.exists('BE/data/userInfo/connections.csv'):
    csv_editor.add_csv_line('BE/data/userInfo/connections.csv', ['record','model'])
######

### ROUTES ###
# GET
@app.route('/', methods=['GET'])
def base_route():
    '''info only'''
    return jsonify('Mateo Sakoman - 1865383')

@app.route('/data/record', methods=['GET'])
def get_records():
    '''Returns all uploaded records and if they have a connected model'''
    return data_handler.get_records()

@app.route('/data/model', methods=['GET'])
def get_models():
    '''Returns all uploaded models and their connected model'''
    return data_handler.get_models()

@app.route('/data/record/<file_name>/<id>/lime', methods=['GET'])
def get_lime(file_name, id):
    '''Returns the LIME explanation for a given record instance'''
    return lime_handler.explanation(file_name, id)

# POST
@app.route('/data/record', methods=['POST'])
def upload_record():
    '''Uploads a record'''
    response = file_handler.upload_file(app, '../data/record')
    if response.success == False:
        abort(response.code, response.message)
    return response.__dict__, response.code

@app.route('/data/model', methods=['POST'])
def upload_model():
    '''Uploads a model'''
    response = file_handler.upload_file(app, '../data/model')
    if response.success == False:
        abort(response.code, response.message)
    return response.__dict__, response.code

@app.route('/data/user-info/connection', methods=['POST'])
def upload_user_info_connection():
    '''Edits the connection.csv'''
    response = file_handler.edit_connection(request.json)
    if response.success == True:
        return response.__dict__
    abort(response.code, response.message)

@app.route('/data/user-info/evaluation/<file_name>', methods=['POST'])
def upload_user_info_evaluation(file_name):
    '''Updates the evaluation file for a given record'''
    data = request.json
    path = 'BE/Data/UserInfo/Evaluation/' + file_name + '.csv'
    response = csv_editor.add_csv_line(path, data)

    if response.success == True:
        return response.__dict__
    abort(response.code, response.message)

# DELETE
@app.route('/data/record/<file_name>', methods=['DELETE'])
def delete_record(file_name):
    '''Removes a record and the corresponding data'''
    response = file_handler.delete_file('BE/data/record', file_name)
    if response.success == False:
        abort(response.code, response.message)
    return response.__dict__, response.code

@app.route('/data/model/<file_name>', methods=['DELETE'])
def delete_model(file_name):
    '''Removes a model and the corresponding data'''
    response = file_handler.delete_file('BE/data/model', file_name)
    if response.success == False:
        abort(response.code, response.message)
    return response.__dict__, response.code
######

if __name__ == '__main__':
    app.run(debug=True)