# train_model.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Step 1: Load Dataset
data_path = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\processed_network_data.csv"
data = pd.read_csv(data_path)

print("Original Dataset Shape:", data.shape)  # Debugging: Check dimensions
print("Columns:", data.columns)  # Debugging: Verify column names

# Step 2: Handle Missing Values (Only Numeric Columns)
numeric_cols = data.select_dtypes(include=['number']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())  # Avoiding errors from timestamps

# Step 3: Convert Timestamps (If Available)
if 'timestamp' in data.columns:  # Modify if timestamps are named differently
    data['timestamp'] = pd.to_datetime(data['timestamp'])  # Convert string to datetime format
    data['hour'] = data['timestamp'].dt.hour
    data['minute'] = data['timestamp'].dt.minute
    data['day_of_week'] = data['timestamp'].dt.dayofweek
    data = data.drop(columns=['timestamp'])  # Drop original timestamp column

print("Processed Data Shape:", data.shape)  # Debugging: After preprocessing

# Step 4: Train Unsupervised Anomaly Detection Model
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(data)  # Train model without labels

# Step 5: Save Model
os.makedirs("models", exist_ok=True)  # Ensure models/ directory exists
model_path = "models/anomaly_detector.pkl"
joblib.dump(model, model_path)

print(f"Unsupervised Model trained and saved successfully at: {model_path}")