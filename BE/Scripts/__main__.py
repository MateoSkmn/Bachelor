### IMPORTS ###
from flask import Flask, jsonify
from flask_cors import CORS
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
    return jsonify("Alle Datensätze")

@app.route('/data/model', methods=['GET'])
def get_models():
    return jsonify("Alle Modelle")

@app.route('/data/records/<file_name>/<id>/lime', methods=['GET'])
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
    return jsonify("Delete Record: " +  file_name)

@app.route('/data/model/<file_name>', methods=['DELETE'])
def delete_model(file_name):
    return jsonify("Delete Model: " +  file_name)
######

if __name__ == '__main__':
    app.run(debug=True)