import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from Utils.Raw_Data import extract_features
PCAP_FILE = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\captured_traffic.pcap"  # Path to your pcap file


def extract_new_features(df):
    """
    Adds new features for ML-based anomaly detection.
    
    Args:
        df (pd.DataFrame): Raw network traffic data.
    
    Returns:
        pd.DataFrame: Enhanced dataset with new features.
    """

    # Convert timestamp to datetime format
    def convert_timestamp(ts):
        try:
            # Try converting as a UNIX timestamp (seconds)
            return pd.to_datetime(ts, unit="s")
        except (ValueError, TypeError):
            # Fallback to direct conversion
            return pd.to_datetime(ts, errors="coerce")

    df["timestamp"] = df["timestamp"].apply(convert_timestamp)


    # Create flow duration feature (time difference between first & last packet)
    df["flow_duration"] = df.groupby(["src_ip", "dst_ip"])["timestamp"].transform(lambda x: (x.max() - x.min()).total_seconds())

    # Compute packet rate (packets per second)
    df["packet_rate"] = df.groupby(["src_ip", "dst_ip"])["timestamp"].transform(
    lambda x: x.count() / (x.max() - x.min()).total_seconds() if x.max() != x.min() else 0
)

    return df

def preprocess_data(df, save_csv=True):
    """
    Prepares raw network data for ML-based anomaly detection and saves it to CSV.
    
    Args:
        df (pd.DataFrame): Raw network traffic data.
        save_csv (bool): Whether to save the processed data as a CSV file.
    
    Returns:
        pd.DataFrame: Processed and normalized dataset.
    """

    print("🔄 Preprocessing data...")
    # Feature Engineering: Extract new features
    df = extract_new_features(df)

    # Convert categorical data (IP addresses, protocol) into numerical labels
    label_encoders = {}
    categorical_columns = ["src_ip", "dst_ip", "protocol"]

    for col in categorical_columns:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        label_encoders[col] = encoder  # Store encoders for later use

    # Normalize numerical data
    scaler = StandardScaler()
    numeric_columns = ["packet_size", "flow_duration", "packet_rate"]
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Optionally, save the preprocessed data back to a CSV file
    if save_csv:
        output_path = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\processed_network_data.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ Processed data saved as '{output_path}'")

    return df, label_encoders, scaler  # Return processed data + encoders for later use


# Fetch the dataframe from pyshark_analysis.py
df_data = extract_features(PCAP_FILE)  # Replace CSV reading with function call
df_data = preprocess_data(df_data, save_csv=True)  # Call the preprocessing function
print("✅ Data preprocessing completed.")