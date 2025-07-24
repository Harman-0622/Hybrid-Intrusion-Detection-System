# Known attack signatures
ATTACK_SIGNATURES = [
    {"src_ip": "192.168.1.100", "desc": "Suspicious internal attacker"},
    {"dst_ip": "10.0.0.1", "desc": "Possible DDoS target"},
    {"protocol": "HTTP", "desc": "Possible web attack"}
]

def detect_attacks(packet_data):
    """
    Checks packets against known attack signatures.

    :param packet_data: List of parsed packet information.
    :return: List of detected alerts.
    """
    alerts = []

    for packet in packet_data:
        for signature in ATTACK_SIGNATURES:
            match_found = all(packet.get(key) == value for key, value in signature.items() if key in packet)

            if match_found:
                alert_msg = f"🚨 Alert: {signature['desc']} detected! Packet: {packet}"
                alerts.append(alert_msg)

    return alerts
