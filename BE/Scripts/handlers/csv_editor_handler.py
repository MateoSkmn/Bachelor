### IMPORTS ###
import csv
from helper.response import Response
######

def find_csv_line_index(file_path, search_value):
    '''
    Find the index of a line in a CSV file based on column values.

    Parameters:
        file_path (str): The path to the CSV file\n
        search_value (dict): A dictionary containing 'index' and 'value' key:
                            'index' specifies the column index to search in\n
                            'value' specifies the value to search for in the column

    Returns:
        Integer of the index the line was found in, -1 otherwise.
    '''
    try:
        # Read the CSV file and search for the line index
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            # Go through text of the file trying to find a line that fits
            for idx, row in enumerate(reader):
                if row[search_value['index']] == search_value['value']:
                    return idx
        return -1
    except IOError:
        print('Error: File not found or unable to read.')
        return -1

def edit_csv_line(file_path, search_value, new_data):
    '''
    Edit a line of a CSV file

    Parameters:
        file_path (str): The path to the CSV file\n
        search_value (dict): A dictionary containing 'index' and 'value' key:
                            'index' specifies the column index to search in\n
                            'value' specifies the value to search for in the column
        new_data (list): The new data to replace the line with.
    
    Returns:
        Response to indicate success
    '''
    line_index = find_csv_line_index(file_path, search_value)
    if line_index != -1:
        return edit_csv_line_by_index(file_path, line_index, new_data)
    else:
        return Response(False, 404, 'Line with specified values not found.')

def edit_csv_line_by_index(file_path, line_index, new_data):
    '''
    Edit line in a CSV file based on its index.

    Parameters:
        file_path (str): The path to a CSV file
        line_index (int): The index of the line to be edited
        new_data (list): The new data to replace the line with
    
    Return:
        Response to indicate success
    '''
    try:
        # Read the existing CSV file
        with open(file_path, 'r', newline='') as file:
            lines = list(csv.reader(file))

        # Check if the line_index is within the range of lines
        if 0 <= line_index < len(lines):
            # Replace the line with new_data
            lines[line_index] = new_data

            # Write the updated data back to the CSV file
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

            return Response(True, 200, 'Connection edited.')
        else:
            return Response(False, 400, 'Line index is out of range.')
    except FileNotFoundError:
        print('Error: File not found.')
        return Response(False, 404, 'File not found.')
    except PermissionError:
        print('Error: Permission denied to read/write the file.')
        return Response(False, 403, 'Permission denied to read/write the file.')
    except Exception as e:
        print(f'Error: {e}')
        return Response(False, 500, 'An unexpected error occurred.')

def add_csv_line(file_path, data):
    '''
    Add a new line to a CSV file. Also creates the file when the path doesn't exist.

    Parameters:
        file_path (str): The path to the CSV file.
        data (list): The data to add as a new line.
    
    Returns:
        Response to indicate success
    '''
    try:
        # Append (a) data to csv file
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return Response(True, 200, 'Added line to csv')
    except Exception as e:
        return Response(False, 500, f'Unexpected error occured: {e}')

def remove_csv_line(file_path, search_value):
    '''
    Remove line from a CSV file based on column values.

    Parameters:
        file_path (str): The path to a CSV file.
        search_value (dict): A dictionary containing 'index' and 'value' key.
                            'index' specifies the column index to search in.
                            'value' specifies the value to search for in the column.
    
    Returns:
        Response to indicate success
    '''
    line_index = find_csv_line_index(file_path, search_value)
    if line_index != -1:
        return remove_csv_line_by_index(file_path, line_index)
    else:
        return Response(False, 404, 'Line with specified values not found.')

def remove_csv_line_by_index(file_path, line_index):
    '''
    Removes a line from a CSV file based on its index.

    Parameters:
        file_path (str): The path to a CSV file
        line_index (int): The index of the line that should be removed
    
    Returns:
        Respone to indicate success
    '''
    try:
        # Read the existing CSV file
        with open(file_path, 'r', newline='') as file:
            lines = list(csv.reader(file))

        # Check if the line_index is within the range of lines
        if 0 <= line_index < len(lines):
            # Remove the line
            del lines[line_index]

            # Write the updated data back to the CSV file
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)

            return Response(True, 200, 'Connection deleted.')
        else:
            return Response(False, 400, 'Line index is out of range.')
    except Exception as e:
        return Response(False, 500, f'Unexpected error: {e}')
    
def clear_csv(file_path):
    '''
    Delete all entries in a CSV file, keeps the header

    Parameters:
        file_path (str): The path to a CSV file
        line_index (int): The index of the line to remove

    Returns:
        True when successful, False otherwise
    '''
    try:
        # Read the existing CSV file
        with open(file_path, 'r', newline='') as file:
            lines = list(csv.reader(file))
        
        # Remember the header for later
        lines = [lines[0]]

        # Write header back into the file, removing everything else
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

        return True

    except Exception as e:
        print(f'Unexpected Error: {e}')
        return False
