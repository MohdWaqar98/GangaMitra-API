from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Load model and scaler
model = joblib.load("rf_compressed.pkl")
scaler = joblib.load("input_scaler.pkl")

# Health check route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Model is running ✅"}), 200

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON input
        input_data = request.get_json()

        # Expected order of features
        feature_order = ["NDVI", "TSS", "Temperature", "Precipitation", "Latitude", "Longitude"]

        # Arrange inputs in required order
        X = np.array([[input_data[feature] for feature in feature_order]])

        # Scale the input
        X_scaled = scaler.transform(X)

        # Predict
        prediction = model.predict(X_scaled)[0]

        # Map prediction to output with 2 decimal places
        output = {
            "DO": round(prediction[0], 2),
            "BOD": round(prediction[1], 2),
            "pH": round(prediction[2], 2),
            "TC": round(prediction[3], 2),
            "FC": round(prediction[4], 2)
        }

        return jsonify(output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
