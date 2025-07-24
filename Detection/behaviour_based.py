import sys
import os
import joblib
import pandas as pd
# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "C:\\Users\\harma\\OneDrive\\Desktop\\IDS"))
sys.path.append(project_root)

print("🔄 Loading libraries...")
import pandas as pd
import joblib
from Utils.preprocess import preprocess_data
print("✅ Libraries loaded.")
def detect_anomalies(input_csv, model_path="models/anomaly_detector.pkl"):
    """
    Detects anomalies in network traffic using a trained ML model.
    
    Args:
        input_csv (str): Path to the CSV file containing network traffic data.
        model_path (str): Path to the trained ML model.
    
    Returns:
        pd.DataFrame: Data with anomaly predictions.
    """
   # behaviour_based.py

def detect_anomalies(data_path, model_path="models/anomaly_detector.pkl"):
    # Load dataset
    data = pd.read_csv(data_path)

    # Ensure model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Error: Model file '{model_path}' not found!")

    # Convert `timestamp` into matching features (Ensure consistency)
    if 'timestamp' in data.columns:
        data['timestamp'] = pd.to_datetime(data['timestamp'])  # Convert to datetime
        data['hour'] = data['timestamp'].dt.hour
        data['minute'] = data['timestamp'].dt.minute
        data['day_of_week'] = data['timestamp'].dt.dayofweek
        data = data.drop(columns=['timestamp'])  # Drop original timestamp column

    # Load trained model
    model = joblib.load(model_path)

    # Ensure feature names match before prediction
    trained_features = model.feature_names_in_  # Get expected feature names
    data = data[trained_features]  # Reorder columns to match training features

    # Predict anomalies
    predictions = model.predict(data)

    # Filter anomalies (-1 indicates anomalous instances)
    anomalies_detected = data[predictions == -1]

    return anomalies_detected
# Run behavior-based detection
# Run behavior-based detection
if __name__ == "__main__":
     detect_anomalies("C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\processed_network_data.csv")
