import os
import pyshark
import pandas as pd

# Set capture file path
PCAP_FILE = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\captured_traffic.pcap"
OUTPUT_FOLDER = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data"  # Folder to save the CSV file
INTERFACE = "WiFi"  # Change based on your network interface (Use 'Get-NetAdapter' in PowerShell)

def analyze_pcap(PCAP_FILE):
    """
    Extracts key information from a .pcap file using PyShark.

    :param pcap_file: Path to the .pcap file.
    :return: List of parsed packet information.
    """
    packet_data = []

    try:
        capture = pyshark.FileCapture(PCAP_FILE)

        for packet in capture:
            try:
                timestamp = packet.sniff_time
                src_ip = packet.ip.src if hasattr(packet, 'ip') else "N/A"
                dst_ip = packet.ip.dst if hasattr(packet, 'ip') else "N/A"
                protocol = packet.highest_layer

                packet_info = {
                    "timestamp": str(timestamp),
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "protocol": protocol
                }

                packet_data.append(packet_info)

            except AttributeError:
                continue

        capture.close()

    except Exception as e:
        print(f"Error analyzing pcap file: {e}")

    return packet_data

def extract_features(PCAP_FILE):
    """
    Extracts features from a .pcap file and saves them to a CSV file in the Captured_Data folder.

    :param PCAP_FILE: Path to the .pcap file.
    :return: DataFrame containing the extracted features.
    """
    capture = pyshark.FileCapture(PCAP_FILE, display_filter="tcp or udp")
    data = []
    
    for packet in capture:
        try:
            features = {
                "src_ip": packet.ip.src,
                "dst_ip": packet.ip.dst,
                "src_port": packet[packet.transport_layer].srcport,
                "dst_port": packet[packet.transport_layer].dstport,
                "protocol": packet.transport_layer,
                "packet_size": int(packet.length),
                "timestamp": float(packet.sniff_timestamp)
            }
            data.append(features)
        except AttributeError:
            continue

    capture.close()

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Ensure the output folder exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Save the DataFrame to a CSV file in the output folder
    output_csv = os.path.join(OUTPUT_FOLDER, "network_data.csv")
    df.to_csv(output_csv, index=False)
    print(f"CSV file saved to: {output_csv}")

    return df

# Example usage
df = extract_features(PCAP_FILE)