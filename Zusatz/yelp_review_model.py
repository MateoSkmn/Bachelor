### IMPORT ###
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier 
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
##############
class YelpReviewModel:
    def __init__(self):
        self.pipeline = None
        self.X_test = None
        self.y_test = None
    
    def train(self):
        data = pd.read_csv("BE/data/Yelp Restaurant Reviews.csv")

        X, y = data["Review Text"], data["Rating"]
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
        X_train_vectorized = vectorizer.fit_transform(X_train).toarray()

        param_grid = {
            "min_samples_leaf": [2, 4],
            "class_weight": [None, "balanced"],
            "max_depth": [None, 10, 20, 30],
            "n_estimators": [100, 200]
        }

        clf = RandomForestClassifier()
        grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1)
        print("Fitting started")
        grid_search.fit(X_train_vectorized, y_train)

        best_estimator = grid_search.best_estimator_
        self.pipeline = make_pipeline(vectorizer, best_estimator)

        # Print best parameters and accuracy
        print("Best Parameters:", grid_search.best_params_)
        print("Best Accuracy:", grid_search.best_score_)

        # Evaluate on test set
        y_pred = self.pipeline.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Test Accuracy: {accuracy}")

        print("------- Training completed -------")
        with open('BE/model/Yelp Restaurant Reviews.csv.pkl', 'wb') as f:
            pickle.dump(self.pipeline, f)
        print("------- File saved -------")
#############
    def test(self):
        data = pd.read_csv("BE/data/Yelp Restaurant Reviews.csv")
        filtered_data = data[data['Rating'] == 1]
        print(filtered_data.head())
    

if __name__ == '__main__':
    clf = YelpReviewModel()
    clf.train()
    #clf.test()