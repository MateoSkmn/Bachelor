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
    #TODO: Refactor
    model_name = data_handler.get_model_by_record_connection(file_name)
    file_path = 'BE/Data/Model/' + model_name
    with open(file_path , 'rb') as f:
        loaded_model: Pipeline = pickle.load(f)

    understandable, prediction = data_handler.get_user_data(file_name, id)

    record_directory = 'BE/Data/Record/'

    data = pd.read_csv(record_directory + file_name)
    X, y = data["Review Text"], data["Rating"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    index = int(id)

    class_names = ['1', '2', '3', '4', '5']
    explainer = LimeTextExplainer(class_names=class_names, random_state=42)
    text = X_test.iloc[index]
    exp = explainer.explain_instance(text, loaded_model.predict_proba, num_features=10, labels=[0,1,2,3,4])

    text = X_test.iloc[index]
    actual_label = int(y_test.iloc[index])
    all_values = [exp.as_list(label=label) for label in range(5)]
    model_prediction_label = int(loaded_model.predict([text])[0])
    lime_prediction_label = int(class_names[np.argmax(exp.predict_proba)])
    max_index = len(X_test) - 1

    word_info_list = __calculate_lime_alpha_values(all_values)

    response_data = {
        "text": text,
        "lime_values": word_info_list,
        "actual_label": actual_label,
        "model_predicted_label": model_prediction_label,
        "lime_predicted_label": lime_prediction_label,
        "user_predicted_label": prediction,
        "user_understandable": understandable,
        "max_index": max_index
    }

    return response_data

def __calculate_lime_alpha_values(all_values):
    word_info = {}
    # Find the maximum value across all lists
    max_value = max(max(value for _, value in lime_list) for lime_list in all_values)
    
    for idx, lime_list in enumerate(all_values):
        for word, value in lime_list:
            if value > 0:  # Skip negative values
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