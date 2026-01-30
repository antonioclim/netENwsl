#!/usr/bin/env python3
"""
Exercise 3: Packet Sniffer (Educational)
========================================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES (Anderson-Bloom Taxonomy):
1. UNDERSTAND how packet capture works at the network layer
2. APPLY BPF filters to capture specific traffic
3. ANALYSE captured packets to identify protocols and payloads
4. COMPARE plaintext vs encrypted traffic patterns
5. EVALUATE security implications of observable metadata

PAIR PROGRAMMING NOTES:
- Driver: Implement packet handling, configure capture filters
- Navigator: Cross-reference with Wireshark, verify captured data
- Swap after: Successfully capturing and displaying MQTT packets

IMPORTANT:
Packet capture typically requires elevated privileges. On Linux, run with sudo:
    sudo python3 ex_13_03_packet_sniffer.py --iface any --timeout 20

This tool is intended for local laboratory use only.

USAGE:
    # Capture Week 13 lab traffic
    python3 ex_13_03_packet_sniffer.py --iface any --timeout 30

    # Capture with custom filter
    python3 ex_13_03_packet_sniffer.py --iface eth0 --bpf "tcp port 1883"

    # Save to PCAP file
    python3 ex_13_03_packet_sniffer.py --iface any --pcap-out capture.pcap
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import datetime as _dt
import binascii
from typing import Optional

SCAPY_AVAILABLE = True
try:
    from scapy.all import sniff, wrpcap  # type: ignore
    from scapy.layers.inet import IP, TCP, UDP  # type: ignore
except ImportError:  # pragma: no cover
    SCAPY_AVAILABLE = False
    sniff = wrpcap = IP = TCP = UDP = None  # type: ignore


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_AND_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Port to protocol label mapping for Week 13 services
PORT_LABELS = {
    21: "FTP",
    80: "HTTP",
    1883: "MQTT",
    2121: "FTP-Lab",
    6200: "BACKDOOR-STUB",
    8080: "DVWA",
    8883: "MQTT-TLS",
}

# Default BPF filter targeting Week 13 lab ports
DEFAULT_BPF = (
    "tcp port 1883 or tcp port 8883 or tcp port 80 or "
    "tcp port 8080 or tcp port 21 or tcp port 2121 or tcp port 6200"
)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def now_ts() -> str:
    """Return current timestamp for logging."""
    return _dt.datetime.now().strftime("%H:%M:%S.%f")[:-3]


def label_port(port: int) -> str:
    """
    Get human-readable label for a port number.
    
    Args:
        port: Port number
    
    Returns:
        Service label or empty string if unknown
    """
    return PORT_LABELS.get(port, "")


def payload_snippet(pkt, max_bytes: int = 32) -> Optional[str]:
    """
    Extract a snippet of the TCP payload for display.
    
    💭 PREDICTION: Will this function show anything for TLS traffic?
       (Answer: Only encrypted bytes - no readable content)
    
    Args:
        pkt: Scapy packet with TCP layer
        max_bytes: Maximum bytes to extract
    
    Returns:
        String representation of payload (text or hex) or None
    """
    try:
        raw = bytes(pkt[TCP].payload)
    except Exception:
        return None
    
    if not raw:
        return None
    
    snip = raw[:max_bytes]
    
    # Try to decode as text, fall back to hex
    try:
        txt = snip.decode("utf-8")
        # Escape control characters for display
        txt = txt.replace("\r", "\\r").replace("\n", "\\n")
        return f"text:{txt}"
    except Exception:
        return f"hex:{binascii.hexlify(snip).decode()}"


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def handle_packet(pkt) -> None:
    """
    Process and display information about a captured packet.
    
    💭 PREDICTION: What information will be visible for MQTT over TLS (port 8883)?
       (Answer: IP addresses, ports, packet size - but NOT topic or message content)
    
    This function extracts:
    - Source and destination IP addresses
    - Transport protocol (TCP/UDP)
    - Source and destination ports
    - Known service labels
    - Payload snippet for plaintext protocols
    
    Args:
        pkt: Scapy packet object
    """
    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACT_IP_LAYER
    # ─────────────────────────────────────────────────────────────────────────
    if IP not in pkt:
        return  # Skip non-IP packets

    ip = pkt[IP]
    proto = "IP"
    src = ip.src
    dst = ip.dst

    sport = dport = None
    
    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACT_TRANSPORT_LAYER
    # ─────────────────────────────────────────────────────────────────────────
    if TCP in pkt:
        proto = "TCP"
        l4 = pkt[TCP]
        sport = int(l4.sport)
        dport = int(l4.dport)
    elif UDP in pkt:
        proto = "UDP"
        l4 = pkt[UDP]
        sport = int(l4.sport)
        dport = int(l4.dport)

    # If no transport layer ports, just show IP info
    if sport is None or dport is None:
        print(f"[{now_ts()}] {proto} {src} -> {dst} len={len(pkt)}")
        return

    # ─────────────────────────────────────────────────────────────────────────
    # IDENTIFY_SERVICES
    # ─────────────────────────────────────────────────────────────────────────
    sp = f"{sport}"
    dp = f"{dport}"
    sl = label_port(sport)
    dl = label_port(dport)

    tags = []
    if sl:
        tags.append(sl)
    if dl and dl != sl:
        tags.append(dl)

    tag = f" ({', '.join(tags)})" if tags else ""

    # ─────────────────────────────────────────────────────────────────────────
    # EXTRACT_PAYLOAD_SNIPPET (for plaintext MQTT only)
    # ─────────────────────────────────────────────────────────────────────────
    extra = ""
    if proto == "TCP" and (sport == 1883 or dport == 1883):
        snip = payload_snippet(pkt)
        if snip:
            extra = f" | {snip}"

    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_PACKET_INFO
    # ─────────────────────────────────────────────────────────────────────────
    print(f"[{now_ts()}] {proto} {src}:{sp} -> {dst}:{dp}{tag} len={len(pkt)}{extra}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_CAPTURE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def run_capture(
    interface: str,
    bpf_filter: str,
    timeout: int,
    count: int,
    pcap_out: Optional[str]
) -> int:
    """
    Execute packet capture with specified parameters.
    
    Args:
        interface: Network interface to capture on
        bpf_filter: Berkeley Packet Filter expression
        timeout: Capture duration in seconds
        count: Maximum packets to capture (0 for unlimited)
        pcap_out: Optional path to save PCAP file
    
    Returns:
        Number of packets captured
    """
    print("=" * 72)
    print("Week 13 - Packet Sniffer (Educational)")
    print("=" * 72)
    print(f"Interface: {interface}")
    print(f"Timeout: {timeout}s")
    print(f"Count: {count if count > 0 else 'unlimited'}")
    print(f"BPF filter: {bpf_filter}")
    if pcap_out:
        print(f"PCAP output: {pcap_out}")
    print()
    print("Capturing packets... (Ctrl+C to stop early)")
    print("-" * 72)

    # ─────────────────────────────────────────────────────────────────────────
    # EXECUTE_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    packets = sniff(
        iface=interface,
        filter=bpf_filter,
        prn=handle_packet,
        timeout=timeout,
        count=count if count > 0 else 0,
        store=bool(pcap_out),  # Only store if saving to file
    )

    # ─────────────────────────────────────────────────────────────────────────
    # SAVE_PCAP_FILE (if requested)
    # ─────────────────────────────────────────────────────────────────────────
    if pcap_out and packets:
        wrpcap(pcap_out, packets)
        print(f"\n[+] PCAP written to: {pcap_out}")
        print(f"    Open in Wireshark: wireshark {pcap_out}")

    print("-" * 72)
    print(f"[+] Capture complete. Packets processed: {len(packets)}")
    
    return len(packets)


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 13 - Packet sniffer (educational)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --iface any --timeout 30
  %(prog)s --iface eth0 --bpf "tcp port 1883" --pcap-out mqtt.pcap
  %(prog)s --iface any --count 100

Note: Requires elevated privileges (sudo) on Linux.
        """
    )
    parser.add_argument("--iface", default="any",
                        help="Interface name (default: any)")
    parser.add_argument("--count", type=int, default=0,
                        help="Max packets to capture (0 = unlimited)")
    parser.add_argument("--timeout", type=int, default=20,
                        help="Capture timeout in seconds (default: 20)")
    parser.add_argument("--bpf", default=DEFAULT_BPF,
                        help="BPF filter (default targets Week 13 lab ports)")
    parser.add_argument("--pcap-out", default=None,
                        help="Optional PCAP output path")
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    args = parse_args()

    if not SCAPY_AVAILABLE:
        print("Scapy is required for this exercise")
        print("Install with: pip install scapy")
        return 1
    
    try:
        packet_count = run_capture(
            interface=args.iface,
            bpf_filter=args.bpf,
            timeout=args.timeout,
            count=args.count,
            pcap_out=args.pcap_out
        )
        return 0
    except PermissionError:
        print("\n[ERROR] Permission denied. Run with elevated privileges:")
        print("        sudo python3 ex_13_03_packet_sniffer.py ...")
        return 1
    except KeyboardInterrupt:
        print("\n[INFO] Capture interrupted by user.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
