### IMPORTS ###
import csv
from helper.response import Response
######

def find_csv_line_index(file_path, search_value):
    """
    Find the index of a line in a CSV file based on column values.

    Parameters:
        file_path (str): The path to the CSV file.
        search_value (dict): A dictionary containing 'index' and 'value' key.
                            'index' specifies the column index to search in.
                            'value' specifies the value to search for in the column.

    Returns:
        int: The index of the line if found, -1 otherwise.
    """
    try:
        # Read the CSV file and search for the line index
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if row[search_value['index']] == search_value['value']:
                    return idx
        return -1
    except IOError:
        print("Error: File not found or unable to read.")
        return -1

def edit_csv_line(file_path, search_value, new_data):
    """
    Edit a specific line in a CSV file based on column values.

    Parameters:
        file_path (str): The path to the CSV file.
        search_value (dict): A dictionary containing 'index' and 'value' key.
                            'index' specifies the column index to search in.
                            'value' specifies the value to search for in the column.
        new_data (list): The new data to replace the line with.

    Returns:
        bool: True if the edit was successful, False otherwise.
    """
    line_index = find_csv_line_index(file_path, search_value)
    if line_index != -1:
        return edit_csv_line_by_index(file_path, line_index, new_data)
    else:
        return Response(False, 404, "Line with specified values not found.")

def edit_csv_line_by_index(file_path, line_index, new_data):
    """
    Edit a specific line in a CSV file based on its index.

    Parameters:
        file_path (str): The path to the CSV file.
        line_index (int): The index of the line to edit (0-indexed).
        new_data (list): The new data to replace the line with.

    Returns:
        bool: True if the edit was successful, False otherwise.
    """
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

            return Response(True, 200, "Connection edited.")
        else:
            return Response(False, 400, "Line index is out of range.")
    except FileNotFoundError:
        print("Error: File not found.")
        return Response(False, 404, "File not found.")
    except PermissionError:
        print("Error: Permission denied to read/write the file.")
        return Response(False, 403, "Permission denied to read/write the file.")
    except IOError:
        print("Error: Unable to read/write the file.")
        return Response(False, 500, "Unable to read/write the file.")
    except Exception as e:
        print(f"Error: {e}")
        return Response(False, 500, "An unexpected error occurred.")

def add_csv_line(file_path, data):
    """
    Add a new line to a CSV file.

    Parameters:
        file_path (str): The path to the CSV file.
        data (list): The data to add as a new line.

    Returns:
        bool: True if the addition was successful, False otherwise.
    """
    try:
        # Append data as a new line to the CSV file
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return Response(True, 200, "Added line to csv")
    except IOError:
        return Response(True, 400, "Error: File not found or unable to read/write.")

def remove_csv_line(file_path, search_value):
    """
    Remove a specific line from a CSV file based on column values.

    Parameters:
        file_path (str): The path to the CSV file.
        search_value (dict): A dictionary containing 'index' and 'value' key.
                            'index' specifies the column index to search in.
                            'value' specifies the value to search for in the column.

    Returns:
        bool: True if the removal was successful, False otherwise.
    """
    line_index = find_csv_line_index(file_path, search_value)
    if line_index != -1:
        return remove_csv_line_by_index(file_path, line_index)
    else:
        return Response(False, 404, "Line with specified values not found.")

def remove_csv_line_by_index(file_path, line_index):
    """
    Remove a specific line from a CSV file based on its index.

    Parameters:
        file_path (str): The path to the CSV file.
        line_index (int): The index of the line to remove (0-indexed).

    Returns:
        bool: True if the removal was successful, False otherwise.
    """
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

            return Response(True, 200, "Connection deleted.")
        else:
            return Response(True, 400, "Line index is out of range.")
    except IOError:
        return Response(True, 400, "Error: File not found or unable to read/write.")
    
def clear_csv(file_path):
    """
    Delete all entries in a CSV file except the header

    Parameters:
        file_path (str): The path to the CSV file.
        line_index (int): The index of the line to remove (0-indexed).

    Returns:
        bool: True if the removal was successful, False otherwise.
    """
    try:
        # Read the existing CSV file
        with open(file_path, 'r', newline='') as file:
            lines = list(csv.reader(file))
        
        # Remove all lines except at index 0
        lines = [lines[0]]

        # Write the updated data back to the CSV file
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)

        return True

    except IOError:
        print("Error: File not found or unable to read/write.")
        return False
