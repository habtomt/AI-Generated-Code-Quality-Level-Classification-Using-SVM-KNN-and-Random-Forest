import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Mock Model Setup (In a real scenario, you'd load a pre-trained .pkl file)
MODEL_PATH = 'model.joblib'

def train_and_save_mock_model():
    X, y = make_classification(n_samples=100, n_features=4, n_informative=2, random_state=42)
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    train_and_save_mock_model()

# Load the model into memory
model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to serve model predictions.
    Expects JSON: {"data": [[1.2, 0.5, 2.1, 0.3], [...]]}
    """
    try:
        # Get data from request
        input_json = request.get_json(force=True)
        
        if not input_json or 'data' not in input_json:
            return jsonify({'error': 'No input data provided. Please provide a "data" key.'}), 400

        # Validate input format (expecting list of lists)
        input_data = np.array(input_json['data'])
        
        if input_data.ndim != 2 or input_data.shape[1] != 4:
            return jsonify({'error': 'Invalid input shape. Expected (N, 4).'}), 400

        # Perform prediction
        predictions = model.predict(input_data)
        probabilities = model.predict_proba(input_data)

        # Return results
        return jsonify({
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist(),
            'status': 'success'
        }), 200

    except Exception as e:
        # Generic error handling
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True}), 200

if __name__ == '__main__':
    # Flask's built-in server is threaded by default in modern versions,
    # handling concurrent requests. For production, use Gunicorn/uWSGI.
    app.run(host='0.0.0.0', port=5000, threaded=True)
