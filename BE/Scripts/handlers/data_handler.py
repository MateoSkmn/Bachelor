### IMPORTS ###
import os
import pandas as pd
######

def get_records():
    ''' Return all the record names and if they have a model attached to them'''
    record_list = []
    connections_df = pd.read_csv('BE/data/userInfo/connections.csv')
    for file_name in __allFileNamesSorted('BE/data/record'):
        hasModel = file_name in connections_df['record'].values
        record_list.append({'file_name': file_name, 'hasModel': hasModel})
        
    return record_list

def get_models():
    ''' Return all the models and their corresponding record '''
    model_list = []
    connections_df = pd.read_csv('BE/data/userInfo/connections.csv')
    for file_name in __allFileNamesSorted('BE/data/model'):
        record = connections_df.loc[connections_df['model'] == file_name, 'record'].values
        record_name = record[0] if len(record) > 0 else None
        model_list.append({'file_name': file_name, 'record_name': record_name})
    
    return model_list

def get_model_by_record_connection(record: str):
    '''
    Get the connected model from a record.

    Parameter:
        record (str): Name of the record to search for
    
    Returns:
        The connected model name. None if there is none
    '''
    connections_df = pd.read_csv('BE/data/userInfo/connections.csv')
    filtered_df = connections_df[connections_df['record'] == record]['model']

    if not filtered_df.empty:
        return filtered_df.iloc[0]
    return None

def get_record_by_model_connection(model: str):
    '''
    Get the connected record from a model
    
    Parameter:
        model (str): Name of the model to search for
    
    Returns:
        The connected record name. None if there is none
    '''
    connections_df = pd.read_csv('BE/data/userInfo/connections.csv')
    filtered_df = connections_df[connections_df['model'] == model]['record']
    
    if not filtered_df.empty:
        return filtered_df.iloc[0]
    return None

def get_user_data(file_name, id):
    '''
    Get the evaluation data for a given instance
    
    Parameters:
        file_name (str): Name of the evaluation file
        id (str): ID of the instance
    
    Returns:
        Two values for "understandable" and "prediction". Can be None if there are no values    
    '''
    path = 'BE/data/userInfo/evaluation/' + file_name
    evaluation_df = pd.read_csv(path)
    filtered_df = evaluation_df[evaluation_df['id'] == int(id)]

    if not filtered_df.empty:
        # Extract the second and third values of the first matching row
        understandable = int(filtered_df.iloc[0, 1])
        prediction = int(filtered_df.iloc[0, 2])
        return understandable, prediction
    else:
        return None, None

### HELPER ###
def __allFileNamesSorted(directory):
    '''
    Get all files sorted by upload date. Sorting by date is less confusing in the FE
    
    Parameters:
        directory (str): Name of the directory to look through
    
    Returns:
        List of file names
    '''
    # Get all filenames in the directory with modification times
    file_names_with_mtime = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == '.gitkeep':  # Ignore .gitkeep files
                continue
            file_path = os.path.join(root, file)
            mtime = os.path.getmtime(file_path)
            file_names_with_mtime.append((file, mtime))
    
    # Sort the filenames based on modification time
    sorted_file_names = sorted(file_names_with_mtime, key=lambda x: x[1])
    
    # Extract only the filenames
    sorted_file_names = [os.path.splitext(file[0])[0] + os.path.splitext(file[0])[1] for file in sorted_file_names]

    return sorted_file_names
######