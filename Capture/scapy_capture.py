import os
from scapy.all import sniff, wrpcap

# Set capture file path and folder
OUTPUT_DIR = "Captured_Data"  # Folder to store the .pcap file
PCAP_FILE = os.path.join(OUTPUT_DIR, "captured_traffic.pcap")
INTERFACE = "Wi-Fi"  # Change based on your network interface (Use 'Get-NetAdapter' in PowerShell)

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Function to capture packets using scapy
def packet_handler(packet):
    print(f"Captured: {packet.summary()}")  # Display packet info
    wrpcap(PCAP_FILE, [packet], append=True)  # Save to pcap file

# Function to capture packets in real-time
def capture_traffic():
    print(f"Capturing traffic on {INTERFACE}... Press Ctrl+C to stop.")
    sniff(iface=INTERFACE, prn=packet_handler, store=False)


# Main function to execute the script
if __name__ == "__main__":
        capture_traffic()