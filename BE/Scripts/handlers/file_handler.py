### IMPORTS ###
import os
from flask import request
from helper.response import Response
######

def delete_file(directory, filename):
    # Delete a file in a given directory
    file_path = os.path.join(directory, filename)

    try:
        os.remove(file_path)
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

    return Response(True, 200, 'File uploaded successfully')