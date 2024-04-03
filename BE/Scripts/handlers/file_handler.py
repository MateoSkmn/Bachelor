### IMPORTS ###
import os
from flask import request
from helper.response import Response
import handlers.csv_editor_handler as csv_editor
import handlers.data_handler as data_handler
######

def delete_file(directory, filename):
    # Delete a file in a given directory
    file_path = os.path.join(directory, filename)

    try:
        os.remove(file_path)
        if directory == 'BE/data/record':
            os.remove('BE/Data/UserInfo/Evaluation/' + filename + '.csv')
            csv_editor.remove_csv_line('BE/Data/UserInfo/connections.csv', dict(index=0, value=filename))
        elif directory == 'BE/data/model':
            record_name = data_handler.get_record_by_model_connection(filename)
            evaluation_path = 'BE/Data/UserInfo/Evaluation/' + record_name + '.csv'
            csv_editor.clear_csv(evaluation_path)
            csv_editor.remove_csv_line('BE/Data/UserInfo/connections.csv', dict(index=1, value=filename))
        return Response(True, 200, f"{filename} has been deleted successfully.")
    except FileNotFoundError:
        return Response(False, 404, f"File {filename} not found in directory {directory}.")
    except PermissionError:
        return Response(False, 403, f"Permission denied to delete {filename}.")
    except Exception as e:
        return Response(False, 400, f"An error occurred: {e}")
    
def upload_file(app, folder):
    # Upload a file to a given directory
    if 'file' not in request.files:
        return Response(False, 400, 'No file part')
    
    file = request.files['file']
    if file.filename == '':
        return Response(False, 400, 'No selected file')

    # Create directory if it doesn't exist
    directory = os.path.join(app.root_path, folder)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save the file
    file_path = os.path.join(directory, file.filename)
    file.save(file_path)

    # Create Evaluation csv file for records
    if folder == "../data/record":
        path = "BE/Data/UserInfo/Evaluation/" + file.filename + ".csv"
        header = ["id", "understandable", "prediction"]
        csv_editor.add_csv_line(path, header)

    return Response(True, 200, 'File uploaded successfully')

def edit_connection(data):
    path = "BE/Data/UserInfo/connections.csv"
    search_value = {"index": 0, "value": data[0]}
    # data in format [string, string]
    if len(data) != 2:
        return Response(400, "Connection needs exactly 2 values!")
    # Delete line when no connection is set
    if data[1] == "":
        return csv_editor.remove_csv_line(path, search_value)
    # Edit line if record has changed
    response = csv_editor.edit_csv_line(path, search_value, data)
    if response.success == True:
        return response
    response = csv_editor.add_csv_line(path, data)
    return response