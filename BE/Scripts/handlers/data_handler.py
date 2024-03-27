### IMPORTS ###
import os
import pandas as pd
######

# VARIABLES
# TODO: create file if it doesnt exist
__connections_df = pd.read_csv('BE/data/userInfo/connections.csv')
######

def get_records():
    # Return all the record names and if they have a model
    record_list = []
    for file_name in __allFileNamesSorted('BE/data/record'):
        hasModel = file_name in __connections_df['record'].values
        record_list.append({"file_name": file_name, "hasModel": hasModel})
        
    return record_list

def get_models():
    # Return all the models and their corresponding record
    model_list = []
    for file_name in __allFileNamesSorted('BE/data/model'):
        record = __connections_df.loc[__connections_df['model'] == file_name, 'record'].values
        record_name = record[0] if len(record) > 0 else None
        model_list.append({"file_name": file_name, "record_name": record_name})
    
    return model_list

### HELPER ###
def __allFileNamesSorted(directory) -> list:
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