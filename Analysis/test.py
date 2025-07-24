import os
import pyshark

# Set capture file path
PCAP_FILE = "C:\\Users\\harma\\OneDrive\\Desktop\\IDS\\Captured_Data\\captured_traffic.pcap"
INTERFACE = "WiFi"  # Change based on your network interface (Use 'Get-NetAdapter' in PowerShell)ccccc

# Function to analyze the captured pcap file using pyshark
def analyze_pcap():
    if not os.path.exists(PCAP_FILE):
        print("No capture file found!")
        return


    capture = pyshark.FileCapture(PCAP_FILE)

    for packet in capture:
        try:
            print(f"Packet: {packet.sniff_time} | Length: {packet.length} bytes | Protocol: {packet.highest_layer}")
        except AttributeError:
            continue

    capture.close()
# Main function to execute the script
if __name__ == "__main__":
        analyze_pcap()
      