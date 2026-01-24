#!/usr/bin/env python3
"""
Homework 6.2: ARP Cache Investigation and Anomaly Detection
===========================================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Analyse ARP cache entries and understand their lifecycle
- Detect potential ARP anomalies (duplicate IPs, suspicious MACs)
- Implement basic ARP spoofing detection logic

Level: Intermediate (⭐⭐⭐)
Estimated time: 60-75 minutes

⚠️ ETHICAL NOTE: This exercise is for DEFENSIVE purposes only.
"""

from __future__ import annotations
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Set

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ARPEntry:
    """Represents an ARP cache entry."""
    ip_address: str
    mac_address: str
    interface: str
    state: str
    timestamp: datetime

@dataclass
class ARPAnomaly:
    """Represents a detected ARP anomaly."""
    anomaly_type: str
    severity: str
    description: str
    evidence: List[str]
    recommendation: str

# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
SAMPLE_ARP_CACHE = [
    ARPEntry("192.168.1.1", "00:11:22:33:44:55", "eth0", "REACHABLE", datetime.now()),
    ARPEntry("192.168.1.10", "aa:bb:cc:dd:ee:01", "eth0", "REACHABLE", datetime.now()),
    ARPEntry("192.168.1.20", "aa:bb:cc:dd:ee:02", "eth0", "STALE", datetime.now() - timedelta(minutes=5)),
    # Anomaly: Same MAC for different IPs
    ARPEntry("192.168.1.40", "aa:bb:cc:dd:ee:01", "eth0", "REACHABLE", datetime.now()),
    # Anomaly: Gateway MAC changed
    ARPEntry("192.168.1.1", "ff:ff:ff:ff:ff:01", "eth0", "REACHABLE", datetime.now() + timedelta(seconds=30)),
    # Anomaly: Broadcast MAC in unicast
    ARPEntry("192.168.1.60", "ff:ff:ff:ff:ff:ff", "eth0", "REACHABLE", datetime.now()),
]

KNOWN_DEVICES = {
    "192.168.1.1": {"mac": "00:11:22:33:44:55", "name": "Default Gateway"},
    "192.168.1.10": {"mac": "aa:bb:cc:dd:ee:01", "name": "Web Server"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def normalise_mac(mac: str) -> str:
    """Normalise MAC address to lowercase with colons."""
    clean = mac.lower().replace("-", "").replace(":", "").replace(".", "")
    if len(clean) != 12:
        return mac.lower()
    return ":".join(clean[i:i+2] for i in range(0, 12, 2))

def is_broadcast_mac(mac: str) -> bool:
    """Check if MAC is broadcast address."""
    return normalise_mac(mac) == "ff:ff:ff:ff:ff:ff"

def detect_duplicate_mac(entries: List[ARPEntry]) -> List[ARPAnomaly]:
    """Detect when the same MAC is associated with multiple IPs."""
    anomalies = []
    mac_to_ips: Dict[str, Set[str]] = defaultdict(set)
    
    for entry in entries:
        mac = normalise_mac(entry.mac_address)
        mac_to_ips[mac].add(entry.ip_address)
    
    for mac, ips in mac_to_ips.items():
        if len(ips) > 1 and not is_broadcast_mac(mac):
            anomalies.append(ARPAnomaly(
                anomaly_type="DUPLICATE_MAC",
                severity="HIGH",
                description=f"MAC {mac} is associated with multiple IPs",
                evidence=[f"IPs: {', '.join(sorted(ips))}"],
                recommendation="Investigate for potential ARP spoofing"
            ))
    return anomalies

def detect_gateway_change(entries: List[ARPEntry], known: Dict) -> List[ARPAnomaly]:
    """Detect if gateway MAC has changed."""
    anomalies = []
    gateway_ip = "192.168.1.1"
    
    if gateway_ip not in known:
        return anomalies
    
    known_mac = normalise_mac(known[gateway_ip]["mac"])
    
    for entry in entries:
        if entry.ip_address == gateway_ip:
            current_mac = normalise_mac(entry.mac_address)
            if current_mac != known_mac:
                anomalies.append(ARPAnomaly(
                    anomaly_type="GATEWAY_MAC_CHANGE",
                    severity="CRITICAL",
                    description=f"Gateway MAC changed: {known_mac} → {current_mac}",
                    evidence=[f"Expected: {known_mac}", f"Observed: {current_mac}"],
                    recommendation="IMMEDIATE: Potential ARP spoofing attack!"
                ))
    return anomalies

def detect_broadcast_unicast(entries: List[ARPEntry]) -> List[ARPAnomaly]:
    """Detect broadcast MAC in unicast ARP entry."""
    anomalies = []
    for entry in entries:
        if is_broadcast_mac(entry.mac_address):
            anomalies.append(ARPAnomaly(
                anomaly_type="BROADCAST_IN_UNICAST",
                severity="HIGH",
                description=f"Broadcast MAC for unicast IP {entry.ip_address}",
                evidence=[f"Entry: {entry.ip_address} -> {entry.mac_address}"],
                recommendation="Invalid entry - possible attack"
            ))
    return anomalies

def detect_all_anomalies(entries: List[ARPEntry], known: Dict) -> List[ARPAnomaly]:
    """Run all anomaly detection checks."""
    anomalies = []
    anomalies.extend(detect_duplicate_mac(entries))
    anomalies.extend(detect_gateway_change(entries, known))
    anomalies.extend(detect_broadcast_unicast(entries))
    return anomalies

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_arp_cache(entries: List[ARPEntry]) -> None:
    """Display ARP cache in table format."""
    print("\n" + "=" * 80)
    print("ARP CACHE")
    print("=" * 80)
    print(f"{'IP Address':<16} {'MAC Address':<20} {'State':<12}")
    print("-" * 80)
    for entry in entries:
        print(f"{entry.ip_address:<16} {entry.mac_address:<20} {entry.state:<12}")
    print("=" * 80)

def display_anomalies(anomalies: List[ARPAnomaly]) -> None:
    """Display detected anomalies."""
    if not anomalies:
        print("\n✅ No anomalies detected")
        return
    
    print(f"\n⚠️ ANOMALIES DETECTED: {len(anomalies)}")
    print("=" * 70)
    
    for i, a in enumerate(anomalies, 1):
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(a.severity, "⚪")
        print(f"\n{icon} #{i}: {a.anomaly_type} ({a.severity})")
        print(f"   {a.description}")
        print(f"   Recommendation: {a.recommendation}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 6.2: ARP Cache Investigation")
    print("Computer Networks - Week 6 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    display_arp_cache(SAMPLE_ARP_CACHE)
    anomalies = detect_all_anomalies(SAMPLE_ARP_CACHE, KNOWN_DEVICES)
    display_anomalies(anomalies)
    
    print("\n📝 Defence Recommendations:")
    print("   1. Implement Dynamic ARP Inspection (DAI)")
    print("   2. Use static ARP for critical infrastructure")
    print("   3. Deploy ARP monitoring tools (arpwatch)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
