# visualize_anomalies.py
import pandas as pd
import matplotlib.pyplot as plt
import joblib

def visualize_anomalies(data_path, model_path="models/anomaly_detector.pkl"):
    """Loads data, applies model, and plots anomaly visualization."""
    
    # Load preprocessed network data
    data = pd.read_csv(data_path)

    # Load trained model
    model = joblib.load(model_path)

    # Make predictions (Isolation Forest: 1 = normal, -1 = anomaly)
    predictions = model.predict(data)

    # Create a scatter plot
    plt.figure(figsize=(10, 6))

    # Plot normal instances (blue dots)
    plt.scatter(data.index, model.decision_function(data), c="blue", label="Normal Traffic", alpha=0.6)

    # Plot anomalies (red dots)
    anomalies = data.index[predictions == -1]
    plt.scatter(anomalies, model.decision_function(data)[predictions == -1], c="red", label="Anomalies", marker="x")

    # Labels and formatting
    plt.xlabel("Data Points")
    plt.ylabel("Anomaly Score")
    plt.title("Intrusion Detection: Normal vs Anomalous Traffic")
    plt.legend()

    # Show plot
    plt.show()