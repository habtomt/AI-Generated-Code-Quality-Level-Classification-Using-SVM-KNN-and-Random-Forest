"""
Auto-generated Python code
Scenario : Machine Learning - AI Model Deployment
Prompt   : response_000.txt
Run      : 3
"""

# Import required libraries
from flask import Flask, request, jsonify
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import datasets
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pickle

app = Flask(__name__)

# Load the machine learning model
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    # Train a machine learning model if the file is not found
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    pipe_svc = Pipeline([('scaler', scaler), ('svm', svm.SVC())])

    param_grid = {'svm__C': [1, 5, 10],
                  'svm__kernel': ['linear', 'rbf', 'poly']}

    grid = GridSearchCV(pipe_svc, param_grid, cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)

    model = grid.best_estimator_
    pickle.dump(model, open('model.pkl', 'wb'))

# Define a function to make predictions
def make_prediction(data):
    try:
        prediction = model.predict(data)
        return prediction.tolist()
    except Exception as e:
        return str(e)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the request
        data = request.json['data']

        # Make a prediction
        prediction = make_prediction(data)

        # Return the prediction as JSON
        return jsonify({'prediction': prediction})
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, threaded=True)