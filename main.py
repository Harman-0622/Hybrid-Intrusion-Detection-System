from Capture.scapy_capture import capture_traffic
# Step 1: Capture packets
pcap_file = capture_traffic()  # This should return the path to the captured pcap file
from Analysis.pyshark_analysis import PCAP_FILE, analyze_pcap
from Detection.signature_based import detect_attacks
from Detection.behaviour_based import detect_anomalies
import pandas as pd
from Visualise_anomalies import visualize_anomalies  # Import visualization function


# Step 2: Analyze packets
packet_data = analyze_pcap(PCAP_FILE)  # Ensure this function returns the packet data correctly

# Step 3: Detect attacks using signature-based IDS
alerts = detect_attacks(packet_data)

# Step 4: Display results
if alerts:
    print("\n⚠️  Intrusion Alerts ⚠️")
    for alert in alerts:
        print(alert)
else:
    print("\n✅ No threats detected.")
print("Now performing behaviour based & anomly based detection")

# Load and preprocess data before anomaly detection
data_path = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\processed_network_data.csv"
data = pd.read_csv(data_path)

# Convert timestamps into matching features
if 'timestamp' in data.columns:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['hour'] = data['timestamp'].dt.hour
    data['minute'] = data['timestamp'].dt.minute
    data['day_of_week'] = data['timestamp'].dt.dayofweek
    data = data.drop(columns=['timestamp'])  # Drop original timestamp

# Save the modified dataset temporarily to ensure consistency
preprocessed_data_path = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\preprocessed_network_data.csv"
data.to_csv(preprocessed_data_path, index=False)

# Run anomaly detection on the corrected dataset
anomalies = detect_anomalies(preprocessed_data_path)

# Display detected anomalies
print("Detected Anomalies:")
print(anomalies)

# Provide user option to visualize anomalies
user_choice = input("Do you want to visualize detected anomalies? (yes/no): ").strip().lower()

if user_choice == "yes":
    visualize_anomalies(preprocessed_data_path)
