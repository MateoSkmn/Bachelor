### IMPORTS ###
import os
from flask import request
from helper.response import Response
import handlers.csv_editor_handler as csv_editor
import handlers.data_handler as data_handler
######

def delete_file(directory, filename):
    '''
    Delete a file in a given directory.

    Parameters:
        directory (str): name of the directory => 'BE/data/record' or 'BE/data/model'
        filename (str): name of the file

    Returns:
        Response to show if the request was successfull, un
    '''
    file_path = os.path.join(directory, filename)

    try:
        os.remove(file_path)
        if directory == 'BE/data/record':
            # Deleting a record also deletes the evaluation and the connection
            os.remove('BE/Data/UserInfo/Evaluation/' + filename + '.csv')
            csv_editor.remove_csv_line('BE/Data/UserInfo/connections.csv', dict(index=0, value=filename))
        elif directory == 'BE/data/model':
            # Deleting a model also clears the corresponding evaluation
            record_name = data_handler.get_record_by_model_connection(filename)
            if record_name is not None:
                evaluation_path = 'BE/Data/UserInfo/Evaluation/' + record_name + '.csv'
                csv_editor.clear_csv(evaluation_path)
                csv_editor.remove_csv_line('BE/Data/UserInfo/connections.csv', dict(index=1, value=filename))
        return Response(True, 200, f"{filename} has been deleted successfully.")
    except FileNotFoundError:
        return Response(False, 404, f"File {filename} not found in directory {directory}.")
    except Exception as e:
        return Response(False, 400, f"An error occurred: {e}")
    
def upload_file(app, folder):
    '''
    Upload a file to a given directory.

    Parameters:
        app (Flask): Access to Flask
        folder (str): Folder name
    
    Returns:
        Response to indicate success
    '''
    if 'file' not in request.files:
        return Response(False, 400, 'No file part')
    
    file = request.files['file']
    if file.filename == '':
        return Response(False, 400, 'No selected file')

    try:
        # Create directory if it doesnt exist
        directory = os.path.join(app.root_path, folder)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Save the file
        file_path = os.path.join(directory, file.filename)
        file.save(file_path)
    except Exception as e:
        return Response(False, 400, f"An error occurred: {e}")

    # Create Evaluation csv file for records
    if folder == '../data/record':
        path = 'BE/Data/UserInfo/Evaluation/' + file.filename + '.csv'
        header = ['id', 'understandable', 'prediction']
        csv_editor.add_csv_line(path, header)

    return Response(True, 200, 'File uploaded successfully')

def edit_connection(data):
    '''
    Edit the connection.csv.

    Parameter:
        data (list): String list in form of [record_name, model_name]
    
    Returns:
        Response to indicate success
    '''
    path = 'BE/Data/UserInfo/connections.csv'
    search_value = {'index': 1, 'value': data[1]}
    # data in format [string, string]
    if len(data) != 2:
        return Response(400, 'Connection needs exactly 2 values!')
    # Delete line when no connection is set
    if data[0] == '':
        return csv_editor.remove_csv_line(path, search_value)
    # Edit line if record has changed
    response = csv_editor.edit_csv_line(path, search_value, data)
    if response.success == True:
        return response
    response = csv_editor.add_csv_line(path, data)
    return response