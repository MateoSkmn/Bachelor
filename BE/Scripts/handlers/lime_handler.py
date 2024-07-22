### IMPORTS ###
import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from lime.lime_text import LimeTextExplainer
import handlers.data_handler as data_handler
######

def explanation(file_name, id):
    '''
    Perform a LIME explanation for a given instance.

    Parameters:
        file_name (str): Name of record
        id (str): ID of instance
    
    Returns:
        Dictionary of data containing all needed values
    '''
    # Load saved model
    loaded_model: Pipeline = __load_model(file_name);

    # Perform train test split
    data = pd.read_csv('BE/Data/Record/' + file_name)
    X, y = data['Review Text'], data['Rating']
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    index = int(id)

    # Execute explanation for insatnce using model and fixed class names
    class_names = ['1', '2', '3', '4', '5']
    explainer = LimeTextExplainer(class_names=class_names, random_state=42)
    text = X_test.iloc[index]
    exp = explainer.explain_instance(text, loaded_model.predict_proba, num_features=10, labels=[0,1,2,3,4])

    # Get all values for return
    text = X_test.iloc[index]
    actual_label = int(y_test.iloc[index])
    model_prediction_label = int(loaded_model.predict([text])[0])
    lime_prediction_label = int(class_names[np.argmax(exp.predict_proba)])
    max_index = len(X_test) - 1

    # Adjust LIME values to be more readable
    all_values = [exp.as_list(label=label) for label in range(5)]
    word_info_list = __calculate_lime_alpha_values(all_values)

    # Load user data
    evaluation_name = file_name + '.csv'
    understandable, prediction = data_handler.get_user_data(evaluation_name, id)

    # Hide specific data when the user is not supposed to find out about it
    if understandable is not None:
        response_data = {
            'text': text,
            'lime_values': word_info_list,
            'actual_label': actual_label,
            'model_predicted_label': model_prediction_label,
            'lime_predicted_label': lime_prediction_label,
            'user_predicted_label': prediction,
            'user_understandable': understandable,
            'max_index': max_index
        }
    else:
        response_data = {
            'text': text,
            'lime_values': word_info_list,
            'max_index': max_index
        }

    return response_data

def __calculate_lime_alpha_values(all_values):
    '''
    Calculates the adjusted value for all LIME values for easier access in FE

    Parameter:
        all_values (list): All LIME-values for each of the classifications

    Returns:
        List of words connected to the predicted classification and value 
    '''
    word_info = {}
    # Find the maximum value across all lists
    max_value = max(max(value for _, value in lime_list) for lime_list in all_values)
    
    for idx, lime_list in enumerate(all_values):
        for word, value in lime_list:
            if value > 0:  # Skip negative values as they dont help in understanding the model for multiple classes
                # Adjust the value to be the percentage of the maximum value
                adjusted_value = round(value / max_value, 4) if max_value != 0 else 0
                if word not in word_info or adjusted_value > 0:
                    if word not in word_info:
                        word_info[word] = {'value': adjusted_value, 'index': idx + 1}
                    else:
                        if adjusted_value > word_info[word]['value']:
                            word_info[word]['value'] = adjusted_value
                            word_info[word]['index'] = idx + 1
    word_info_list = [{'word': word, 'index': info['index'], 'value': info['value']} for word, info in word_info.items()]

    return word_info_list

def __load_model(file_name):
    '''
    Load the saved model to use during explanation.

    Parameter:
        file_name (str): record name

    Returns:
        Object of loaded model, should be instantiated as Pipeline
    '''
    model_name = data_handler.get_model_by_record_connection(file_name)
    file_path = 'BE/Data/Model/' + model_name
    with open(file_path , 'rb') as f:
        return pickle.load(f)