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

Level: Advanced (⭐⭐⭐)
Estimated time: 60-75 minutes

Learning Objectives Covered:
- LO1: Recall supporting protocols (ARP)
- LO2: Explain protocol state tables

⚠️ ETHICAL NOTE: This exercise is for DEFENSIVE purposes only.
Understanding attack patterns helps build better network defences.

Usage:
    python homework/exercises/hw_6_02_arp_investigation.py
    python homework/exercises/hw_6_02_arp_investigation.py --verbose
    python homework/exercises/hw_6_02_arp_investigation.py --export report.json
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class ARPState(Enum):
    """ARP cache entry states (Linux kernel)."""
    INCOMPLETE = "INCOMPLETE"  # Resolution in progress
    REACHABLE = "REACHABLE"    # Recently confirmed
    STALE = "STALE"            # Needs reconfirmation
    DELAY = "DELAY"            # Waiting before probe
    PROBE = "PROBE"            # Sending probes
    FAILED = "FAILED"          # Resolution failed
    NOARP = "NOARP"            # No ARP needed (loopback)
    PERMANENT = "PERMANENT"    # Statically configured
    
    @classmethod
    def from_string(cls, value: str) -> "ARPState":
        """Parse state from string with fallback."""
        try:
            return cls(value.upper())
        except ValueError:
            logger.debug(f"Unknown ARP state: {value}")
            return cls.INCOMPLETE


class AnomalySeverity(Enum):
    """Severity levels for detected anomalies."""
    CRITICAL = "CRITICAL"  # Immediate action required
    HIGH = "HIGH"          # Investigate soon
    MEDIUM = "MEDIUM"      # Monitor closely
    LOW = "LOW"            # Informational
    
    def __lt__(self, other: "AnomalySeverity") -> bool:
        """Allow sorting by severity."""
        order = [self.LOW, self.MEDIUM, self.HIGH, self.CRITICAL]
        return order.index(self) < order.index(other)


class AnomalyType(Enum):
    """Types of ARP anomalies."""
    DUPLICATE_MAC = "DUPLICATE_MAC"
    GATEWAY_MAC_CHANGE = "GATEWAY_MAC_CHANGE"
    BROADCAST_IN_UNICAST = "BROADCAST_IN_UNICAST"
    MAC_FLIP_FLOP = "MAC_FLIP_FLOP"
    GRATUITOUS_ARP_STORM = "GRATUITOUS_ARP_STORM"
    VENDOR_MISMATCH = "VENDOR_MISMATCH"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ARPEntry:
    """
    Represents an ARP cache entry.
    
    Attributes:
        ip_address: IPv4 address
        mac_address: MAC address (colon-separated)
        interface: Network interface name
        state: ARP state (REACHABLE, STALE, etc.)
        timestamp: When entry was observed
    """
    ip_address: str
    mac_address: str
    interface: str
    state: ARPState
    timestamp: datetime
    
    def __post_init__(self) -> None:
        """Validate and normalise entry."""
        self.mac_address = MACAddress.normalise(self.mac_address)
        if not self._is_valid_ip(self.ip_address):
            logger.warning(f"Invalid IP address: {self.ip_address}")
    
    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IPv4 address format."""
        if not ip:
            return False
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False
    
    def age_seconds(self) -> float:
        """Calculate age of entry in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "ip": self.ip_address,
            "mac": self.mac_address,
            "interface": self.interface,
            "state": self.state.value,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class ARPAnomaly:
    """
    Represents a detected ARP anomaly.
    
    Attributes:
        anomaly_type: Type of anomaly detected
        severity: How urgent is this finding
        description: Human-readable description
        evidence: List of supporting evidence
        recommendation: Suggested action
        affected_ips: IP addresses involved
        affected_macs: MAC addresses involved
    """
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    description: str
    evidence: List[str]
    recommendation: str
    affected_ips: List[str] = field(default_factory=list)
    affected_macs: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "type": self.anomaly_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "affected_ips": self.affected_ips,
            "affected_macs": self.affected_macs,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class KnownDevice:
    """Represents a known/trusted device."""
    ip: str
    mac: str
    name: str
    is_gateway: bool = False
    vendor: Optional[str] = None


@dataclass
class AnalysisReport:
    """Container for complete analysis results."""
    total_entries: int = 0
    unique_ips: int = 0
    unique_macs: int = 0
    anomalies: List[ARPAnomaly] = field(default_factory=list)
    by_state: Dict[str, int] = field(default_factory=dict)
    by_interface: Dict[str, int] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def has_critical(self) -> bool:
        """Check if any critical anomalies exist."""
        return any(a.severity == AnomalySeverity.CRITICAL for a in self.anomalies)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "summary": {
                "total_entries": self.total_entries,
                "unique_ips": self.unique_ips,
                "unique_macs": self.unique_macs,
                "anomaly_count": len(self.anomalies),
                "has_critical": self.has_critical,
            },
            "by_state": self.by_state,
            "by_interface": self.by_interface,
            "anomalies": [a.to_dict() for a in self.anomalies],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MAC_ADDRESS_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

class MACAddress:
    """Utilities for MAC address handling."""
    
    BROADCAST = "ff:ff:ff:ff:ff:ff"
    MULTICAST_BIT = 0x01
    LOCAL_BIT = 0x02
    
    @classmethod
    def normalise(cls, mac: str) -> str:
        """
        Normalise MAC address to lowercase colon-separated format.
        
        Args:
            mac: MAC in any format (colons, dashes, dots, or none)
            
        Returns:
            Normalised MAC (e.g., "aa:bb:cc:dd:ee:ff")
        """
        # Remove all separators
        clean = mac.lower().replace("-", "").replace(":", "").replace(".", "")
        
        # Validate length
        if len(clean) != 12:
            logger.debug(f"Invalid MAC length: {mac}")
            return mac.lower()
        
        # Validate hex characters
        if not all(c in "0123456789abcdef" for c in clean):
            logger.debug(f"Invalid MAC characters: {mac}")
            return mac.lower()
        
        # Reformat with colons
        return ":".join(clean[i:i+2] for i in range(0, 12, 2))
    
    @classmethod
    def is_broadcast(cls, mac: str) -> bool:
        """Check if MAC is broadcast address."""
        return cls.normalise(mac) == cls.BROADCAST
    
    @classmethod
    def is_multicast(cls, mac: str) -> bool:
        """Check if MAC is multicast (group address)."""
        normalised = cls.normalise(mac)
        if len(normalised) < 2:
            return False
        try:
            first_octet = int(normalised[:2], 16)
            return bool(first_octet & cls.MULTICAST_BIT)
        except ValueError:
            return False
    
    @classmethod
    def is_locally_administered(cls, mac: str) -> bool:
        """Check if MAC is locally administered (not manufacturer-assigned)."""
        normalised = cls.normalise(mac)
        if len(normalised) < 2:
            return False
        try:
            first_octet = int(normalised[:2], 16)
            return bool(first_octet & cls.LOCAL_BIT)
        except ValueError:
            return False
    
    @classmethod
    def get_oui(cls, mac: str) -> str:
        """Get OUI (first 3 octets) for vendor lookup."""
        normalised = cls.normalise(mac)
        return normalised[:8] if len(normalised) >= 8 else ""


# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_ARP_CACHE: List[ARPEntry] = [
    ARPEntry("192.168.1.1", "00:11:22:33:44:55", "eth0", ARPState.REACHABLE, datetime.now()),
    ARPEntry("192.168.1.10", "aa:bb:cc:dd:ee:01", "eth0", ARPState.REACHABLE, datetime.now()),
    ARPEntry("192.168.1.20", "aa:bb:cc:dd:ee:02", "eth0", ARPState.STALE, datetime.now() - timedelta(minutes=5)),
    ARPEntry("192.168.1.30", "aa:bb:cc:dd:ee:03", "eth0", ARPState.REACHABLE, datetime.now()),
    # Anomaly: Same MAC for different IPs (potential MITM)
    ARPEntry("192.168.1.40", "aa:bb:cc:dd:ee:01", "eth0", ARPState.REACHABLE, datetime.now()),
    # Anomaly: Gateway MAC changed (potential ARP spoofing)
    ARPEntry("192.168.1.1", "ff:ff:ff:ff:ff:01", "eth0", ARPState.REACHABLE, datetime.now() + timedelta(seconds=30)),
    # Anomaly: Broadcast MAC in unicast entry (invalid)
    ARPEntry("192.168.1.60", "ff:ff:ff:ff:ff:ff", "eth0", ARPState.REACHABLE, datetime.now()),
]

KNOWN_DEVICES: Dict[str, KnownDevice] = {
    "192.168.1.1": KnownDevice(
        ip="192.168.1.1",
        mac="00:11:22:33:44:55",
        name="Default Gateway",
        is_gateway=True,
        vendor="Cisco"
    ),
    "192.168.1.10": KnownDevice(
        ip="192.168.1.10",
        mac="aa:bb:cc:dd:ee:01",
        name="Web Server",
        vendor="Dell"
    ),
    "192.168.1.2": KnownDevice(
        ip="192.168.1.2",
        mac="00:11:22:33:44:56",
        name="DNS Server",
        vendor="HP"
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# DETECTION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def detect_duplicate_mac(entries: List[ARPEntry]) -> List[ARPAnomaly]:
    """
    Detect when the same MAC is associated with multiple IPs.
    
    This can indicate:
    - ARP spoofing/MITM attack
    - Legitimate: Load balancer, router with multiple IPs
    
    Args:
        entries: List of ARP cache entries
        
    Returns:
        List of detected anomalies
    """
    anomalies: List[ARPAnomaly] = []
    mac_to_ips: Dict[str, Set[str]] = defaultdict(set)
    
    for entry in entries:
        mac = entry.mac_address
        if not MACAddress.is_broadcast(mac):
            mac_to_ips[mac].add(entry.ip_address)
    
    for mac, ips in mac_to_ips.items():
        if len(ips) > 1:
            anomalies.append(ARPAnomaly(
                anomaly_type=AnomalyType.DUPLICATE_MAC,
                severity=AnomalySeverity.HIGH,
                description=f"MAC {mac} is associated with multiple IPs",
                evidence=[
                    f"IPs sharing this MAC: {', '.join(sorted(ips))}",
                    f"Count: {len(ips)} IPs"
                ],
                recommendation="Investigate for potential ARP spoofing or verify if this is a legitimate multi-homed device",
                affected_ips=list(ips),
                affected_macs=[mac]
            ))
    
    return anomalies


def detect_gateway_change(
    entries: List[ARPEntry],
    known_devices: Dict[str, KnownDevice]
) -> List[ARPAnomaly]:
    """
    Detect if gateway MAC has changed from known value.
    
    Gateway MAC changes are CRITICAL as they indicate:
    - Active ARP spoofing attack
    - Router failover (legitimate but should be verified)
    
    Args:
        entries: List of ARP cache entries
        known_devices: Dictionary of known/trusted devices
        
    Returns:
        List of detected anomalies
    """
    anomalies: List[ARPAnomaly] = []
    
    # Find gateway(s) in known devices
    gateways = {ip: dev for ip, dev in known_devices.items() if dev.is_gateway}
    
    for gateway_ip, gateway_info in gateways.items():
        known_mac = MACAddress.normalise(gateway_info.mac)
        
        for entry in entries:
            if entry.ip_address == gateway_ip:
                current_mac = entry.mac_address
                if current_mac != known_mac:
                    anomalies.append(ARPAnomaly(
                        anomaly_type=AnomalyType.GATEWAY_MAC_CHANGE,
                        severity=AnomalySeverity.CRITICAL,
                        description=f"Gateway {gateway_ip} MAC changed!",
                        evidence=[
                            f"Expected MAC: {known_mac} ({gateway_info.name})",
                            f"Observed MAC: {current_mac}",
                            f"Entry state: {entry.state.value}"
                        ],
                        recommendation="IMMEDIATE: Potential ARP spoofing attack. Verify network integrity and investigate source of new MAC.",
                        affected_ips=[gateway_ip],
                        affected_macs=[known_mac, current_mac]
                    ))
    
    return anomalies


def detect_broadcast_unicast(entries: List[ARPEntry]) -> List[ARPAnomaly]:
    """
    Detect broadcast MAC in unicast ARP entry.
    
    This is always invalid and indicates:
    - Malformed ARP response
    - Attack attempt
    
    Args:
        entries: List of ARP cache entries
        
    Returns:
        List of detected anomalies
    """
    anomalies: List[ARPAnomaly] = []
    
    for entry in entries:
        if MACAddress.is_broadcast(entry.mac_address):
            anomalies.append(ARPAnomaly(
                anomaly_type=AnomalyType.BROADCAST_IN_UNICAST,
                severity=AnomalySeverity.HIGH,
                description=f"Broadcast MAC for unicast IP {entry.ip_address}",
                evidence=[
                    f"Entry: {entry.ip_address} → {entry.mac_address}",
                    f"Interface: {entry.interface}",
                    f"State: {entry.state.value}"
                ],
                recommendation="Invalid entry. Remove and investigate source. This should never occur in normal operation.",
                affected_ips=[entry.ip_address],
                affected_macs=[entry.mac_address]
            ))
    
    return anomalies


def detect_all_anomalies(
    entries: List[ARPEntry],
    known_devices: Dict[str, KnownDevice]
) -> List[ARPAnomaly]:
    """
    Run all anomaly detection checks.
    
    Args:
        entries: List of ARP cache entries
        known_devices: Dictionary of known/trusted devices
        
    Returns:
        List of all detected anomalies, sorted by severity
    """
    anomalies: List[ARPAnomaly] = []
    
    # Run all detection functions
    anomalies.extend(detect_duplicate_mac(entries))
    anomalies.extend(detect_gateway_change(entries, known_devices))
    anomalies.extend(detect_broadcast_unicast(entries))
    
    # Sort by severity (critical first)
    anomalies.sort(key=lambda a: a.severity, reverse=True)
    
    return anomalies


def analyse_arp_cache(
    entries: List[ARPEntry],
    known_devices: Dict[str, KnownDevice]
) -> AnalysisReport:
    """
    Perform complete ARP cache analysis.
    
    Args:
        entries: List of ARP cache entries
        known_devices: Dictionary of known/trusted devices
        
    Returns:
        Complete analysis report
    """
    report = AnalysisReport(total_entries=len(entries))
    
    # Collect unique IPs and MACs
    unique_ips: Set[str] = set()
    unique_macs: Set[str] = set()
    
    for entry in entries:
        unique_ips.add(entry.ip_address)
        unique_macs.add(entry.mac_address)
        
        # Count by state
        state = entry.state.value
        report.by_state[state] = report.by_state.get(state, 0) + 1
        
        # Count by interface
        iface = entry.interface
        report.by_interface[iface] = report.by_interface.get(iface, 0) + 1
    
    report.unique_ips = len(unique_ips)
    report.unique_macs = len(unique_macs)
    
    # Detect anomalies
    report.anomalies = detect_all_anomalies(entries, known_devices)
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def display_arp_cache(entries: List[ARPEntry]) -> None:
    """Display ARP cache in table format."""
    print("\n" + "═" * 90)
    print("ARP CACHE")
    print("═" * 90)
    print(f"{'IP Address':<16} {'MAC Address':<20} {'Interface':<10} {'State':<12} {'Age':<10}")
    print("─" * 90)
    
    for entry in entries:
        age = f"{entry.age_seconds():.0f}s ago"
        print(f"{entry.ip_address:<16} {entry.mac_address:<20} {entry.interface:<10} {entry.state.value:<12} {age:<10}")
    
    print("═" * 90)
    print(f"Total entries: {len(entries)}")


def display_anomalies(anomalies: List[ARPAnomaly]) -> None:
    """Display detected anomalies."""
    if not anomalies:
        print("\n✅ No anomalies detected")
        return
    
    print(f"\n⚠️  ANOMALIES DETECTED: {len(anomalies)}")
    print("═" * 75)
    
    severity_icons = {
        AnomalySeverity.CRITICAL: "🔴",
        AnomalySeverity.HIGH: "🟠",
        AnomalySeverity.MEDIUM: "🟡",
        AnomalySeverity.LOW: "🟢",
    }
    
    for i, anomaly in enumerate(anomalies, 1):
        icon = severity_icons.get(anomaly.severity, "⚪")
        print(f"\n{icon} #{i}: {anomaly.anomaly_type.value} ({anomaly.severity.value})")
        print(f"   Description: {anomaly.description}")
        print(f"   Evidence:")
        for evidence in anomaly.evidence:
            print(f"      • {evidence}")
        print(f"   Recommendation: {anomaly.recommendation}")
    
    print("\n" + "═" * 75)


def display_report_summary(report: AnalysisReport) -> None:
    """Display analysis report summary."""
    print("\n" + "═" * 60)
    print("ANALYSIS SUMMARY")
    print("═" * 60)
    
    print(f"\n📊 Statistics:")
    print(f"   Total entries: {report.total_entries}")
    print(f"   Unique IPs: {report.unique_ips}")
    print(f"   Unique MACs: {report.unique_macs}")
    print(f"   Anomalies found: {len(report.anomalies)}")
    
    print(f"\n📈 By State:")
    for state, count in sorted(report.by_state.items()):
        print(f"   {state}: {count}")
    
    if report.has_critical:
        print("\n" + "!" * 60)
        print("!!! CRITICAL ANOMALIES DETECTED - IMMEDIATE ACTION REQUIRED !!!")
        print("!" * 60)


def display_defence_recommendations() -> None:
    """Display defence recommendations."""
    print("\n" + "═" * 60)
    print("📝 DEFENCE RECOMMENDATIONS")
    print("═" * 60)
    recommendations = [
        "1. Implement Dynamic ARP Inspection (DAI) on managed switches",
        "2. Use static ARP entries for critical infrastructure (gateways, servers)",
        "3. Deploy ARP monitoring tools (arpwatch, arpguard)",
        "4. Enable port security on switch ports",
        "5. Use VLANs to segment network and limit broadcast domains",
        "6. Consider 802.1X for network access control",
        "7. Monitor for unusual ARP traffic patterns",
        "8. Keep baseline of known MAC-IP mappings updated",
    ]
    for rec in recommendations:
        print(f"   {rec}")
    print("═" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_report(report: AnalysisReport, path: Path) -> None:
    """Export analysis report to JSON file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\n📁 Report exported to: {path}")
    except IOError as e:
        logger.error(f"Failed to export report: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ARP Cache Investigation — Week 6 Homework"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--export", "-e",
        type=Path,
        help="Export report to JSON file"
    )
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("═" * 70)
    print("Homework 6.2: ARP Cache Investigation")
    print("Computer Networks - Week 6 | ASE Bucharest, CSIE")
    print("═" * 70)
    print("\n⚠️  ETHICAL NOTE: This exercise is for DEFENSIVE purposes only.")
    
    # Display ARP cache
    display_arp_cache(SAMPLE_ARP_CACHE)
    
    # Perform analysis
    report = analyse_arp_cache(SAMPLE_ARP_CACHE, KNOWN_DEVICES)
    
    # Display results
    display_report_summary(report)
    display_anomalies(report.anomalies)
    display_defence_recommendations()
    
    # Export if requested
    if args.export:
        export_report(report, args.export)
    
    # Return code based on findings
    if report.has_critical:
        print("\n❌ CRITICAL anomalies detected - exit code 2")
        return 2
    elif report.anomalies:
        print("\n⚠️  Anomalies detected - exit code 1")
        return 1
    else:
        print("\n✅ No anomalies detected - exit code 0")
        return 0


if __name__ == "__main__":
    sys.exit(main())
