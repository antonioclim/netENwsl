#!/usr/bin/env python3
"""
Exercise 6.01: NAT/PAT Topology
===============================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Topology:
    (private)                      (public)
   h1 ───┐                        ┌─── h3
        s1 ─── rnat ─── s2 ───────┘
   h2 ───┘

Addressing:
- h1: 192.168.1.10/24   gw 192.168.1.1
- h2: 192.168.1.20/24   gw 192.168.1.1
- rnat(private): 192.168.1.1/24
- rnat(public): 203.0.113.1/24  (TEST-NET-3, RFC 5737)
- h3: 203.0.113.2/24    gw 203.0.113.1

Objectives:
- Demonstrate PAT translation (MASQUERADE)
- Observe the difference between private and public addresses
- Understand the NAT table and bidirectional mapping

Prerequisites:
- Mininet installed in WSL/Docker environment
- Root privileges (sudo)

Level: Intermediate
Estimated time: 40 minutes

Pair Programming Notes:
- Driver: Execute commands in Mininet CLI
- Navigator: Verify outputs match predictions
- Swap after: Configuring NAT rules

Usage:
    sudo python3 ex_6_01_nat_topology.py --cli     # Interactive mode
    sudo python3 ex_6_01_nat_topology.py --test    # Automated smoke test
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Private network (RFC 1918)
PRIVATE_SUBNET = "192.168.1.0/24"
H1_IP = "192.168.1.10"
H2_IP = "192.168.1.20"
ROUTER_PRIVATE_IP = "192.168.1.1"

# Public network (TEST-NET-3, RFC 5737 - safe for documentation)
PUBLIC_SUBNET = "203.0.113.0/24"
ROUTER_PUBLIC_IP = "203.0.113.1"
H3_IP = "203.0.113.2"


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER_NODE_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class LinuxRouter(Node):
    """
    Mininet node configured as a Linux router.
    
    Enables IP forwarding and provides cleanup for NAT rules.
    This demonstrates how a Linux box can act as a router/NAT gateway.
    """
    
    def config(self, **params) -> None:
        super().config(**params)
        # Enable IPv4 forwarding - required for routing between interfaces
        self.cmd("sysctl -w net.ipv4.ip_forward=1")

    def terminate(self) -> None:
        # Clean up iptables rules on shutdown
        self.cmd("iptables -t nat -F 2>/dev/null || true")
        self.cmd("iptables -F 2>/dev/null || true")
        super().terminate()


# ═══════════════════════════════════════════════════════════════════════════════
# TOPOLOGY_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════

class NatTopology(Topo):
    """
    NAT topology with:
    - 2 private hosts (h1, h2)
    - 1 Linux router with NAT (rnat)
    - 1 "public" host (h3)
    - 2 OVS switches (s1 private, s2 public)
    """
    
    def build(self) -> None:
        # Switches
        s1 = self.addSwitch("s1")  # Private network
        s2 = self.addSwitch("s2")  # Public network
        
        # Linux router with NAT
        rnat = self.addNode("rnat", cls=LinuxRouter)
        
        # Hosts
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        
        # Links
        self.addLink(h1, s1)       # h1-eth0 ↔ s1
        self.addLink(h2, s1)       # h2-eth0 ↔ s1
        self.addLink(s1, rnat)     # rnat-eth0 (private)
        self.addLink(rnat, s2)     # rnat-eth1 (public)
        self.addLink(s2, h3)       # h3-eth0 ↔ s2


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def configure_network(net: Mininet) -> None:
    """
    Configure IP addresses, routes and NAT rules.
    
    This function demonstrates:
    1. Configuring addresses on specific interfaces
    2. Adding default routes (default gateway)
    3. Configuring NAT with iptables (MASQUERADE)
    """
    h1, h2, h3 = net.get("h1", "h2", "h3")
    rnat = net.get("rnat")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: IP address configuration
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: After this step, what IP will h1 have? What about rnat?
    
    # Private network (192.168.1.0/24)
    h1.setIP(f"{H1_IP}/24", intf="h1-eth0")
    h2.setIP(f"{H2_IP}/24", intf="h2-eth0")
    rnat.setIP(f"{ROUTER_PRIVATE_IP}/24", intf="rnat-eth0")
    
    # Public network (203.0.113.0/24 - TEST-NET-3)
    rnat.setIP(f"{ROUTER_PUBLIC_IP}/24", intf="rnat-eth1")
    h3.setIP(f"{H3_IP}/24", intf="h3-eth0")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 2: Route configuration
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: Without a default route, can h1 reach h3? Why not?
    
    # Private hosts use rnat as default gateway
    h1.cmd(f"ip route add default via {ROUTER_PRIVATE_IP}")
    h2.cmd(f"ip route add default via {ROUTER_PRIVATE_IP}")
    # Public host also uses rnat (for simplicity in this lab)
    h3.cmd(f"ip route add default via {ROUTER_PUBLIC_IP}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 3: NAT configuration (iptables)
    # ─────────────────────────────────────────────────────────────────────────
    
    # 💭 PREDICTION: What source IP will h3 see when h1 sends a packet?
    
    # Clear existing rules to avoid duplication
    rnat.cmd("iptables -t nat -F")
    rnat.cmd("iptables -F")
    
    # Allow forwarding between interfaces
    rnat.cmd("iptables -A FORWARD -i rnat-eth0 -o rnat-eth1 -j ACCEPT")
    rnat.cmd("iptables -A FORWARD -i rnat-eth1 -o rnat-eth0 "
             "-m state --state ESTABLISHED,RELATED -j ACCEPT")
    
    # NAT MASQUERADE for traffic from private network
    # MASQUERADE: automatically uses the outgoing interface's IP
    rnat.cmd(f"iptables -t nat -A POSTROUTING -o rnat-eth1 "
             f"-s {PRIVATE_SUBNET} -j MASQUERADE")
    
    info("*** NAT configuration complete\n")
    info(f"*** h1/h2 ({PRIVATE_SUBNET}) → NAT → {ROUTER_PUBLIC_IP} → h3\n")


# ═══════════════════════════════════════════════════════════════════════════════
# SMOKE_TEST
# ═══════════════════════════════════════════════════════════════════════════════

def run_smoke_test(net: Mininet) -> int:
    """
    Run basic tests to verify functionality.
    
    Returns:
        0 if all tests pass, 1 otherwise
    """
    h1, h2, h3 = net.get("h1", "h2", "h3")
    rnat = net.get("rnat")
    
    # 💭 PREDICTION: Will h1's ping to h3 succeed? What IP will h3 see?
    
    info("\n*** TEST 1: Ping h1 → h3 (through NAT)\n")
    out1 = h1.cmd(f"ping -c 2 -W 2 {H3_IP}")
    ok1 = "0% packet loss" in out1 or "2 received" in out1
    info(f"    Result: {'OK' if ok1 else 'FAIL'}\n")
    
    info("*** TEST 2: Ping h2 → h3 (through NAT)\n")
    out2 = h2.cmd(f"ping -c 2 -W 2 {H3_IP}")
    ok2 = "0% packet loss" in out2 or "2 received" in out2
    info(f"    Result: {'OK' if ok2 else 'FAIL'}\n")
    
    info("*** TEST 3: Verify NAT table\n")
    nat_table = rnat.cmd("iptables -t nat -L -n -v")
    ok3 = "MASQUERADE" in nat_table
    info(f"    MASQUERADE present: {'OK' if ok3 else 'FAIL'}\n")
    
    info("\n*** NAT table (rnat):\n")
    info(nat_table + "\n")
    
    # 💭 PREDICTION: How many conntrack entries will exist after these pings?
    
    info("*** Conntrack table (showing NAT translations):\n")
    conntrack = rnat.cmd("conntrack -L 2>/dev/null || cat /proc/net/nf_conntrack 2>/dev/null || echo 'conntrack not available'")
    info(conntrack[:500] + "\n")  # Truncate for readability
    
    if ok1 and ok2 and ok3:
        info("*** ALL TESTS PASSED ***\n")
        return 0
    else:
        info("*** SOME TESTS FAILED ***\n")
        if not ok1:
            info(f"    h1 ping output: {out1}\n")
        if not ok2:
            info(f"    h2 ping output: {out2}\n")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE_CLI
# ═══════════════════════════════════════════════════════════════════════════════

def print_cli_banner() -> None:
    """Print helpful information when entering CLI mode."""
    info("\n" + "=" * 60 + "\n")
    info("  NAT/PAT TOPOLOGY STARTED\n")
    info("=" * 60 + "\n\n")
    
    info("💭 PREDICTIONS to verify:\n")
    info("  1. What IP will h3 see as source when h1 pings it?\n")
    info("  2. Will h1 and h2 have the same or different translated ports?\n")
    info("  3. Can h3 initiate a connection TO h1? Why or why not?\n\n")
    
    info("Useful commands:\n")
    info("  h1 ping 203.0.113.2              # Ping through NAT\n")
    info("  rnat iptables -t nat -L -n -v    # Show NAT rules\n")
    info("  rnat conntrack -L                # Show NAT translations\n")
    info("  h3 tcpdump -ni h3-eth0 icmp      # Capture on public side\n")
    info("\n" + "=" * 60 + "\n\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mininet topology for NAT/PAT demonstration"
    )
    parser.add_argument(
        "--cli", action="store_true",
        help="Launch interactive Mininet CLI"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run automated smoke test"
    )
    args = parser.parse_args()
    
    # Build topology
    topo = NatTopology()
    net = Mininet(
        topo=topo,
        controller=None,      # No SDN controller needed
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True      # Predictable MACs
    )
    
    net.start()
    
    try:
        configure_network(net)
        
        if args.test:
            return run_smoke_test(net)
        elif args.cli:
            print_cli_banner()
            CLI(net)
        else:
            info("Topology started. Use --cli for interactive mode.\n")
        
        return 0
    finally:
        net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    sys.exit(main())
