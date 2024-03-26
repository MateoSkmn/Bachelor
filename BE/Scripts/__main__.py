### IMPORTS ###
from flask import Flask, jsonify
from flask_cors import CORS
######

### SETUP ###
app = Flask(__name__)
CORS(app, origins=['http://localhost:4200', 'http://localhost:4200/*'])
######

### ROUTES ###
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify('Mateo Sakoman - 1865383')

@app.route('/data/record', methods=['GET'])
def get_records():
    return jsonify("Alle Datensätze")

@app.route('/data/model', methods=['GET'])
def get_models():
    return jsonify("Alle Modelle")
######

if __name__ == '__main__':
    app.run(debug=True)